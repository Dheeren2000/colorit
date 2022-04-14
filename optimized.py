from math import degrees
import psycopg2
import psycopg2.extras
from flask import *
import re


class db_connection:
    def connection():
        
        DB_HOST = "localhost"
        DB_PORT = "5432"
        DB_NAME = "test_color"
        DB_USER = "postgres"
        DB_PASS = "jayesh"

        db_connection.connection.conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
        print('connection successfull')
        

    
    def register():
        db_connection.register.msg = ''
        msg1 = ''
        cursor = db_connection.connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
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
                    db_connection.connection.conn.commit()
                    msg = 'You have successfully registered !'
                else:
                    msg = 'Password and confirm password doesnot match!'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
    
    def login():
        cursor = db_connection.connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
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
        

    
    def dashboard():

        cursor = db_connection.register.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        user_email = session['email']

        cursor.execute('select * from app_users where email=%s',(user_email,))
        user_data = cursor.fetchone()
        firstname = user_data['fname']
        lastname = user_data['lname']

