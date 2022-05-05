import base64
from email.headerregistry import HeaderRegistry
import io
from PIL import Image
from flask import *
import psycopg2
import secrets
import psycopg2.extras
import re
from postgres.ConnectionManager import ConnectionManager
from optimized import db_connection as dbc
import os
from werkzeug.utils import secure_filename
import keras
from skimage.io import imsave
import time 
from utils.Colorizer import Colorizer 
from flask_mail import *
from random import *


model_path = "static\model\Colorizer_ResidualAutoEncoder_100_500.h5"
colorizerModel = keras.models.load_model(model_path)


app = Flask(__name__)
app.secret_key = 'admin_dhc'

#upload img documentation
UPLOAD_FOLDER = 'static/cache/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



#mailing system ****************
mail = Mail(app)

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]= 'test.aiml00@gmail.com'
app.config["MAIL_PASSWORD"]= 'test.aiml@1234'
app.config["MAIL_USE_TLS"]=False 
app.config["MAIL_USE_SSL"]=True
app.config["MAIL_DEFAULT_SENDER"]= 'test.aiml00@gmail.com'
mail = Mail(app)
otp=randint(000000,999999)
#mail systems ends****************************************


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

# Todo : method to colorize the image and send the unique id to the user
@app.route('/colorize', methods=['POST'])
def colorizeImage():

    if request.method == 'POST' and 'image-file' in request.files:

        # getting the file out of the request
        imageFile = request.files['image-file']
        print(f'ImageFile Contents : {imageFile}')

        # saving the file in cache
        imageFileName = secure_filename(imageFile.filename)
        print(f'Name of the ImageFile : {imageFileName}')
        grayFilePath = os.path.join(app.config['UPLOAD_FOLDER'], imageFileName)
        print(f'Path to save imagefile : {grayFilePath}')
        imageFile.save(grayFilePath)

        # checking whether given file is grayscale or not 
        # isGrayScale = ImageUtils.isGrayImage(grayFilePath)
        isGrayScale = True
        print(f'Is GrayScale Image : {isGrayScale}')

        # if grayscale then returning the unvalid image response
        res = None
        if not isGrayScale:
            res = {
                'status' : -9999,
                'uid' : None,
                'message' : 'Not-GrayScale'
            }
            print(f'Removing the "{grayFilePath}" : Not-Grayscale')
            os.remove(grayFilePath)
        else:           # else colorizing the image

            # generating the unique token
            unique_id = secrets.token_hex(16)
            # file path for the colored image
            colorFilePath = os.path.join(app.config['UPLOAD_FOLDER'],'c_' + imageFileName)

            # coloring the grayscale image
            start = time.time()
            rgbResult = Colorizer().predictRGB(model=colorizerModel, imgPath=grayFilePath)
            end = time.time()

            temp = end-start
            print(f'Total Time in Seconds : {temp} sec')
            hours = temp//3600
            temp = temp - 3600*hours
            minutes = temp//60
            seconds = temp - 60*minutes
            print('Total Time Taken : ')
            print('HH:MM:SS => %d:%d:%d' %(hours, minutes, seconds))

            # saving the image
            imsave(colorFilePath, rgbResult)

            # converting the images into the binary files   
            _grayBin = convertToBinary(grayFilePath)
            _colorBin = convertToBinary(colorFilePath)

            # inserting the images in the db
            cursor = conn.cursor()
            cursor.execute('INSERT INTO imagedata (grayImage, rgbImage, fileName, userId, uniqueId) VALUES(%s,%s,%s,%s,%s)', 
                            (psycopg2.Binary(_grayBin), psycopg2.Binary(_colorBin), imageFileName, session['id'], unique_id))
            conn.commit()


            # removing the files from the cache 
            if os.path.exists(grayFilePath):
                os.remove(grayFilePath)
            if os.path.exists(colorFilePath):
                os.remove(colorFilePath)
                    
            res = {
                'status' : 9999,
                'uid' : unique_id,
                'message' : 'GrayScale'
            }

        print(res)
        return jsonify(res)

    return redirect(url_for('dashboard'))
    

# Todo : method to get the uid on colorize page 
@app.route('/displayImage', methods=['POST'])
def renderColorize():

    if request.method == 'POST' and 'image-id' in request.form:
        
        # getting the image id to be displayed 
        imageId = request.form['image-id']

        results = {
            'image-id' : imageId
        }

        return render_template('colorize.html', data=results)
    
    else:
        print('This is exe')
        return redirect(url_for('dashboard'))


# Todo : method to get the uid on colorize page 
@app.route('/getImageData', methods=['POST'])
def returnImageData():

    if request.method == 'POST' and 'image-id' in request.form:
        
        # getting the image id to be displayed 
        imageId = request.form['image-id']

        print(imageId)

        # fetching the image data from the DB
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM imagedata WHERE uniqueId = %s',(imageId,))
        imageData = cursor.fetchone()

        print(imageData)

        # getting all the data out of imageData
        grayBinData = imageData[1]
        colorBinData = imageData[2]
        imageFileName = imageData[3]    # file name
        dataTime = imageData[5]

        # reading the bytes of grayscale image
        grayBytes = io.BytesIO(grayBinData)
        grayBytes.seek(0)
        gray_base64 = base64.b64encode(grayBytes.read())

        # reading the bytes of color image
        colorBytes = io.BytesIO(colorBinData)
        colorBytes.seek(0)
        color_base64 = base64.b64encode(colorBytes.read())

        results = {
            'image-id': imageId,
            'file-name': imageFileName,
            'gray-image': str(gray_base64),
            'color-image': str(color_base64),
            'timeStamp': dataTime
        }

        return jsonify(results)

    else:
        print('load Images not exe')
        return redirect(url_for('dashboard'))

# To download the images
@app.route('/download', methods=['POST'])
def downloadImageFile():

    if request.method == 'POST' and 'image-id' in request.form and 'mode' in request.form:

        # getting the image id and mode to fetch the record 
        imageId = request.form['image-id']
        imageMode = request.form['mode']

        # fetching the image data from the DB
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM imagedata WHERE uniqueId = %s',(imageId,))
        imageData = cursor.fetchone()

        print(imageData)

        # getting all the data out of imageData
        grayBinData = imageData[1]      # gray image binary
        colorBinData = imageData[2]     # color image binary
        imageFileName = imageData[3]    # file name

        if imageMode == 'g':            # sending the grayscale image
            grayBytes = io.BytesIO(grayBinData)
            grayBytes.seek(0)
            return send_file(grayBytes, as_attachment=True, download_name=imageFileName)

        else:                           # sending the color image
            colorBytes = io.BytesIO(colorBinData)
            colorBytes.seek(0)
            return send_file(colorBytes, as_attachment=True, download_name=imageFileName)
        
    return redirect(url_for('redirect_Dashboard'))


# to return to the dashboard from the colorize page
@app.route('/ret_dashboard')
def redirect_Dashboard():
    for fileName in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'],fileName))
    return redirect(url_for('dashboard'))

# ---------------------------------------------------------

# to redirect to the gallery
@app.route('/gallery')
def redirect_gallery():

    # checking if there is session set or not
    if 'email' in session:
        return render_template('gallery.html')

    return redirect(url_for('dashboard'))


# route to return the user images in batches of 4
@app.route('/getUserImages', methods=['POST'])
def returnUserImages():

    if request.method == 'POST' and 'page-no' in request.form:
        # getting the page no out of the form
        pageNo = request.form['page-no']
    
        # setting up the limit 
        limit = 4
        offset = (int(pageNo) - 1) * limit

        # fetching the count of image data from the DB
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT COUNT(*) FROM imagedata WHERE userid = %s ',(session['id'],))
        imageDataCount = cursor.fetchone()[0]

        pageCount = imageDataCount // limit
        if imageDataCount % 4 != 0:
             pageCount += 1
        
        print(f'ImageCount : {imageDataCount} | PageCount : {pageCount}')

        # fetching the image data from the DB
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT fileName, grayImage, rgbImage, uniqueId, to_char(datetime, 'DD Mon YYYY, HH:MI AM') FROM ImageData WHERE userid = %s ORDER BY datetime DESC LIMIT %s OFFSET %s",
        (session['id'], limit, offset))
        records = cursor.fetchall()

        imageData = list()
        for data in records:
            
            # gettting the content out of it
            fileName = data[0]
            grayBinData = data[1]
            colorBinData = data[2]
            uid = data[3]
            udate = data[4].split(', ')[0]
            utime = data[4].split(', ')[1]

            # reading the bytes of grayscale image
            grayBytes = io.BytesIO(grayBinData)
            grayBytes.seek(0)
            gray_base64 = base64.b64encode(grayBytes.read())

            # reading the bytes of color image
            colorBytes = io.BytesIO(colorBinData)
            colorBytes.seek(0)
            color_base64 = base64.b64encode(colorBytes.read())

            result = {
                'uid' : uid,
                'grayImg' : str(gray_base64),
                'colorImg' : str(color_base64),
                'filename' : fileName,
                'upload-date' : udate,
                'upload-time' : utime,
            }

            imageData.append(result)

        res = {
            'fileCount' : imageDataCount,
            'pageCount' : pageCount,
            'data': imageData
        }

        return jsonify(res)

    
    return redirect(url_for('dashboard')) 


# to delete the given image from the gallery
@app.route('/deleteImages', methods=['POST'])
def deleteImages():

    if request.method == 'POST' and 'image-id' in request.form:

        # getting the image-id 
        imgId = request.form['image-id']

        # deleting the record from the table
        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('DELETE FROM ImageData WHERE uniqueId = %s', (imgId,))
            conn.commit()
        except:
            return jsonify({
                'success' : False
            })


        return jsonify({
              'success' : True  
            })

    return redirect(url_for('dashboard'))



# ---------------------------------------------------------
# to change the passoword of the given user
@app.route('/resetPassword', methods=['POST'])
def resetPassword():
    
    if request.method == 'POST' and 'current-password' in request.form and 'new-password' in request.form:
        
        oldPassword = request.form['current-password']
        newPassword = request.form['new-password']

        # checking if the old password is same as in the db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('select * from app_users where email=%s',(session['email'],))
        accountInfo = cursor.fetchone()

        print(f'Account Info : {accountInfo}')
        if accountInfo is not None:
            res = {
                'current-match' : True,
                'new-match' : False,
                'success' : False
            }

            password = accountInfo['password']
            if password != oldPassword:
                res['current-match'] = False
                return jsonify(res)
            
            if password == newPassword:
                res['new-match'] = True
                return jsonify(res)
            else:

                try:
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    cursor.execute('UPDATE app_users SET password=%s WHERE email=%s',
                                    (newPassword, session['email']))
                    conn.commit()
                    res['success'] = True
                    print('Updated Password')
                except:
                    res['success'] = False


                return jsonify(res)            
    else:
        print('Not Executing')
        return redirect(url_for('dashboard'))



@app.route('/forgot_password', methods=['POST', 'GET'])
def forgot_password():
    error = ""
    message = ""
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'enterEmail' in request.form:
        mail1 = request.form['enterEmail']

        cursor.execute('select * from app_users where email=%s', (mail1,))
        account = cursor.fetchone()

        if not account:
            error = 'Account not found!'
        else:
            msg = Message(subject='OTP Verification from ColorIt.io to reset Password', sender='test.aiml00@gmail.com', recipients=[mail1])
            msg.body=str(otp)
            mail.send(msg) 
            message = 'Account Found and mail has been send to the registered email address'
            session['loggedin'] = True
            session['email1'] = request.form['enterEmail']
            return redirect(url_for('verifyotp'))     
    return render_template('forgotpassword.html', error=error,message=message)

@app.route('/verifyotp', methods=['POST', 'GET'])
def verifyotp():
    error = ""
    message = ""
    if request.method == 'POST' and 'otp' in request.form:
        verifyotp = request.form['otp']
        if otp == int(verifyotp):
            return redirect(url_for('changepassword'))
        else:
            return "<h3>please try again</h3>"
    return render_template('verifyOtp.html')

@app.route('/changepassword', methods=['POST', 'GET'])
def changepassword():
    error = ""
    message = ""
    emailId = session['email1']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'enterpass' in request.form and 'verifyenterpass' in request.form:
        changepass = request.form['enterpass']
        verifyChangepass = request.form['verifyenterpass']
        if changepass == verifyChangepass:
            cursor.execute('UPDATE app_users SET password = %s WHERE email = %s', (changepass,emailId))
            conn.commit()
            message = 'password updated successfully'
            return redirect(url_for('login'))
        else:
            error = 'password doesnot match'
            return redirect('changepassword')
    return render_template('changepassword.html')



if __name__ == "__main__":
    app.run(debug=True)