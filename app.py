from flask import *
#from flask_sqlalchemy import SQLAlchemy
import psycopg2
import secrets
import psycopg2.extras
import re
from postgres.ConnectionManager import ConnectionManager
from optimized import db_connection as dbc
import os
import base64
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'admin_dhc'

#upload img documentation
UPLOAD_FOLDER = 'cache/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



# DB_HOST = "localhost"
# DB_PORT = "5432"
# DB_NAME = "db_colorization"
# DB_USER = "postgres"
# DB_PASS = "djmn@1234"

# conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

# getting the postgress connection
conn = ConnectionManager().getConnection()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login' , methods=['POST', 'GET'])
def login():

    #*******************************************for user registration ********************************
    msg = ''
    msg1 = ''
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'Fname' in request.form and 'Lname' in request.form and 'user_email' in request.form and 'password' in request.form and 'confirm_pass' in request.form:
        firstname = request.form['Fname']
        lastname = request.form['Lname']
        emailid = request.form['user_email']
        password = request.form['password']
        confirm_password = request.form['confirm_pass']
        
        cursor.execute('select * from app_users where email=%s',(emailid,))
        account = cursor.fetchone()
        print(account)

        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailid):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-za-z]+' ,firstname):
            msg = 'Name should not contain numbers'
        elif not re.match(r'[A-za-z]+' ,lastname):
            msg = 'Name should not contain numbers'
        elif not password or not emailid:
            msg = 'Please fill out the form !'
        else:
            if password == confirm_password:
                cursor.execute('INSERT INTO app_users (fname,lname,email,password) VALUES (%s, %s, %s, %s)', (firstname, lastname, emailid, password, ))
                conn.commit()
                msg = 'You have successfully registered !'
            else:
                msg = 'Password and confirm password doesnot match!'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'

#****************************************User Login*********************************************************************
    if request.method == 'POST' and 'Email_login' in request.form and 'password_login' in request.form:
        email_login = request.form['Email_login']
        password_login = request.form['password_login']

        cursor.execute('select * from app_users where email=%s and password=%s',(email_login,password_login,))
        account1 = cursor.fetchone()
        print(account1)

        if account1:
            session['loggedin'] = True
            session['id'] = account1['id']
            session['email'] = account1['email']
            msg1 = 'Logged in successfully !'
            return redirect(url_for('dashboard'))
        else:
            msg = 'Incorrect username / password !'
            


    return render_template('login_signup.html', msg=msg)

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop("email", None)
        return render_template("index.html")
    else:
        return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    user_email = session['email']

    cursor.execute('select * from app_users where email=%s',(user_email,))
    user_data = cursor.fetchone()
    firstname = user_data['fname']
    lastname = user_data['lname']

    if session['loggedin'] == True:
        return render_template('dashboard.html',firstname=firstname,lastname=lastname)

@app.route('/dashboard2')
def dashboard2():
    # cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # user_email = session['email']

    # cursor.execute('select * from app_users where email=%s',(user_email,))
    # user_data = cursor.fetchone()
    # firstname = user_data['fname']
    # lastname = user_data['lname']

    return render_template('dashboard2.html')
    #return render_template('dashboard.html',firstname=firstname,lastname=lastname)


#**************************************************upload img code**************************************************
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def convertToBinary(filename):
    with open(filename,'rb') as file:
        binarydata= file.read()
    return binarydata
    
def convertBinarytoFile(binarydata,filename):
    with open(filename,'wb') as file:
        file.write(binarydata)


# @app.route('/uploadImage', methods=['POST','GET'])
# def uploadImage():
#     return render_template('upload_imagePage.html')


# @app.route('/uploadImage_success', methods=['POST','GET'])
# def upload_Image_success():
#     msg=''
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     if 'file' not in request.files:
#         msg = 'no file part'
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename=='':
#         msg = 'no image selected for uploading'
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         msg = 'image successfully uploaded'
#         convertPic = convertTobinary(filename)
#         cursor.execute('Insert into Save_image (Image) values (%s)', (convertPic))
#         conn.commit()
#         msg = 'image successfully uploaded'
#         return render_template('upload_imagePage.html', filename=filename, msg=msg)
        
#     else:
#         return redirect(request.url)
    
# @app.route('/display')
# def display_image(filename):
    
#     return redirect(url_for('static', filename='images/' + filename), code=301, filename=filename)

@app.route('/colorize', methods=['POST'])
def render_colorizerPage():
    
    if request.method == 'POST' and 'img_filename' in request.files:
        file = request.files['img_filename']
        filename = secure_filename(file.filename)
        filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filePath)
        convertPic = convertToBinary(filePath)

        print(f'name of file : {filename}')

        print('Session ID for the user : {}'.format(session['id']))

        # generating the unique id for the given tuple
        unique_id = secrets.token_hex(16)
        print(unique_id)

        # inserting the file into database 
        cursor = conn.cursor()
        cursor.execute('INSERT INTO imagedata (grayImage, rgbImage, fileName, userId, uniqueId) VALUES(%s,%s,%s,%s,%s)', 
                        (psycopg2.Binary(convertPic), psycopg2.Binary(convertPic), filename, session['id'], unique_id))
        conn.commit()

        # removing the original file
        os.remove(filePath)

        # fetching the image data from the DB
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM imagedata WHERE uniqueId = %s',(unique_id,))
        imageData = cursor.fetchone()
        print(imageData[1])
        print(imageData)
        convertBinarytoFile(imageData[1],os.path.join(app.config['UPLOAD_FOLDER'],imageData[3]))
        convertBinarytoFile(imageData[2],os.path.join(app.config['UPLOAD_FOLDER'],'c_' + imageData[3]))
        return render_template('colorize.html', data=unique_id)
    return redirect(url_for('dashboard'))




if __name__ == "__main__":
    app.run(debug=True)