from flask import *
import psycopg2
import psycopg2.extras
import re
from ConnectionManager import ConnectionManager

class Services(ConnectionManager):
    
    def __init__(self) :
        self.msg=""
        
    
    def loginService(self):
        self.msg=""
        cursor = ConnectionManager.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
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
                self.msg = 'Logged in successfully !'
                return redirect(url_for('dashboard'))
            else:
                self.msg = 'Incorrect username / password !'

    def registerService(self):
        self.msg=""
        cursor = ConnectionManager.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
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
                self.msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailid):
                self.msg = 'Invalid email address !'
            elif not re.match(r'[A-za-z]+' ,firstname):
                self.msg = 'Name should not contain numbers'
            elif not re.match(r'[A-za-z]+' ,lastname):
                self.msg = 'Name should not contain numbers'
            elif not password or not emailid:
                self.msg = 'Please fill out the form !'
            else:
                if password == confirm_password:
                    cursor.execute('INSERT INTO app_users (fname,lname,email,password) VALUES (%s, %s, %s, %s)', (firstname, lastname, emailid, password, ))
                    ConnectionManager.conn.commit()
                    self.msg = 'You have successfully registered !'
                else:
                    self.msg = 'Password and confirm password doesnot match!'
        elif request.method == 'POST':
            self.msg = 'Please fill out the form !'

        def getAllImages():
            pass

        def insertImages():
            pass

        def editPassword():
            pass

        def deleteImages():
            pass
