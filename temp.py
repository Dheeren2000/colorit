from flask import *
import psycopg2
import psycopg2.extras
import re
from ConnectionManager import ConnectionManager
from services import Services

app = Flask(__name__)

app.secret_key = 'admin_dhc'
cm = ConnectionManager()
serv = Services()

if cm.getConnection():
    print('connection_successfull')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login' , methods=['POST', 'GET'])
def login():
    serv.registerService()
    if serv.loginService():
        return redirect(url_for('dashboard'))
    return render_template('login_signup.html')

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
    # cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # user_email = session['email']

    # cursor.execute('select * from app_users where email=%s',(user_email,))
    # user_data = cursor.fetchone()
    # firstname = user_data['fname']
    # lastname = user_data['lname']

    return render_template('dashboard.html')
    #return render_template('dashboard.html',firstname=firstname,lastname=lastname)

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

@app.route('/uploadImage')
def uploadImage():
    return render_template('upload_imagePage.html')

if __name__ == "__main__":
    app.run(debug=True)
