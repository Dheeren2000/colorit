import base64
import io
from subprocess import CREATE_NEW_CONSOLE
from cv2 import imread
from flask import *
import secrets
import re

from models.ImageData import ImageData
from models.User import User
import os
from werkzeug.utils import secure_filename
import keras
from skimage.io import imsave
import time
from services.Services import Services 
from utils.Colorizer import Colorizer 
from flask_mail import *
from random import *
from utils.ImageUtils import ImageUtils

from utils.OtpGenerator import OtpGenerator
from utils.Security import Security


model_path = "static\model\Colorizer_ResidualAutoEncoder_1200_500.h5"
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

#mail systems ends****************************************


@app.route('/')
def index():
    return render_template('index.html')


# function to redirect to login-signup page
@app.route('/login-signup', methods=['GET', 'POST'])
def redirect_login_signup():
    return render_template('login_signup.html')

# function to login the user 
@app.route('/login', methods=['POST'])
def userLogin():

    msg = ''
    if request.method == 'POST' and 'Email_login' in request.form and 'password_login' in request.form:

        # getting the email and password for login
        email_login = request.form['Email_login']
        password_login = request.form['password_login']

        account = Services.loginService(email_login, password_login)

        print(account)

        if account:
            session['loggedin'] = True
            session['id'] = account.id
            session['email'] = account.email
            session['first-name'] = account.firstName
            session['last-name'] = account.lastName

            return redirect(url_for('dashboard'))

        else:
            msg = 'Incorrect username / password !'
    return render_template('login_signup.html',  msg=msg)

# function to register user 
@app.route('/register', methods=['POST'])
def userRegistration():
    if request.method == 'POST' and 'Fname' in request.form and 'Lname' in request.form and 'user_email' in request.form and 'password' in request.form and 'confirm_pass' in request.form:

        # getting the data from the requst
        firstname = request.form['Fname']
        lastname = request.form['Lname']
        emailid = request.form['user_email']
        password = request.form['password']
        confirm_password = request.form['confirm_pass']
        
        account = Services.isUserExits(emailid)

        if account is not None:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailid):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-za-z]+' ,firstname):
            msg = 'Name should not contain numbers'
        elif not re.match(r'[A-za-z]+' ,lastname):
            msg = 'Name should not contain numbers'
        elif not re.match(r'^([A-Za-z0-9_\.@\$!]{8,20})$', password):
            msg = 'Password should be alphanumeric and atleast contain 8 characters along with special characters.'
        elif not password or not emailid:
            msg = 'Please fill out the form !'
        else:
            if password == confirm_password:
                
                result = Services.registerService(User(firstname, lastname, emailid, password))

                if result:
                    msg = 'You have successfully registered !'
                else:
                    msg = 'Registration Failed, unable to register'
            else:
                msg = 'Password and confirm password doesnot match!'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return render_template('login_signup.html',  msg=msg)


@app.route("/logout", methods=["POST", "GET"])
def logout():

    if "email" in session:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop("email", None)
        session.pop('first-name', None)
        session.pop("last-name", None)
        
        return render_template("index.html")
    else:
        return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    
    user_email = session['email']
    result = {
        'firstname' : session['first-name'],
        'lastname' : session['last-name']
    }
    
    if session['loggedin'] == True:
        return render_template('dashboard.html', data=result)

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

        # checking if the image size is less than or equal to 720 x 480
        img = imread(grayFilePath)

        print(img.shape)

        img_h = img.shape[0]
        img_w = img.shape[1]

        if img_h > 480 or img_w > 720:
            res = {
                'status' : -8888,
                'uid' : None,
                'message' : 'Size-exceed'
            }
            print(f'Removing the "{grayFilePath}" : Size-exceed')
            os.remove(grayFilePath)
            return jsonify(res)

        # checking whether given file is grayscale or not 
        isGrayScale = ImageUtils.isGrayImage(grayFilePath)
        # isGrayScale = True
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

            user = Services.isUserExits(session['email'])
            imageData = ImageData(fileName=imageFileName, grayImage=_grayBin, rgbImage=_colorBin, uniqueId=unique_id)

            result = Services.insertImage(user, imageData)

            if result:
                print("ImageData inserted successfully")


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

    print('image-id' in request.form)
    if request.method == 'POST' and 'image-id' in request.form:
        
        # getting the image id to be displayed 
        imageId = request.form['image-id']

        preRoute = str(request.referrer).split('/')[-1]
        print('pre-route :', preRoute)
        results = {
            'image-id' : imageId,
            'pre-route' : preRoute
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

        print('Image ID :', imageId)

        imageData = Services.getImageDataByUniqueId(imageId)

        if imageData is None:
            return redirect(url_for('dashboard')) 

        # getting all the data out of imageData
        grayBinData = imageData.grayImage
        colorBinData = imageData.rgbImage
        imageFileName = imageData.fileName    # file name
        datetime = imageData.datetime

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
            'timeStamp': datetime
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

        imageData = Services.getImageDataByUniqueId(imageId)

        # getting all the data out of imageData
        grayBinData = imageData.grayImage     # gray image binary
        colorBinData = imageData.rgbImage     # color image binary
        imageFileName = imageData.fileName    # file name

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

    if request.method == 'POST' and 'page-no' in request.form and 'search-name' in request.form:
        # getting the page no out of the form
        pageNo = request.form['page-no']
        searchName = request.form['search-name']
        # print(f'SearchName = {searchName}')

        # setting up the limit 
        limit = 4
        offset = (int(pageNo) - 1) * limit

        imageDataCount, records = Services.getUserImages(searchName, session['id'], limit, offset)

        pageCount = imageDataCount // limit
        if imageDataCount % 4 != 0:
             pageCount += 1
        
        # print(f'ImageCount : {imageDataCount} | PageCount : {pageCount}')

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

        result = Services.deleteImages(imgId)

        if result:
            return jsonify({
              'success' : True  
            })
            
        else:
             return jsonify({
                'success' : False
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
        accountInfo = Services.isUserExits(session['email'])

        print(f'Account Info : {accountInfo}')
        if accountInfo is not None:
            res = {
                'current-match' : True,
                'new-match' : False,
                'success' : False
            }

            password = Security.dcryptData(accountInfo.password)
            if password != oldPassword:
                res['current-match'] = False
                return jsonify(res)
            
            if password == newPassword:
                res['new-match'] = True
                return jsonify(res)
            else:

                if Services.editPassword(session['email'], newPassword):    
                    res['success'] = True
                    print('Updated Password')
                else:
                    res['success'] = False


                return jsonify(res)            
    else:
        print('Not Executing')
        return redirect(url_for('dashboard'))

# forget password -----------------------------------------------------------------------------

@app.route('/forgot_password', methods=['POST','GET'])
def forgot_password():
    error = ""
    message = ""

    if request.method == 'POST' and 'enterEmail' in request.form:
        mail1 = request.form['enterEmail']

        account = Services.isUserExits(mail1)

        if not account:
            error = 'Account not found!'
        else:
            
            otp = OtpGenerator.getRandomOtp()
                
            msg = Message(subject='OTP Verification from ColorIt.io to reset Password', sender='test.aiml00@gmail.com', recipients=[mail1])
            msg.body= "OTP : " + otp
            mail.send(msg) 
            message = 'Account Found and mail has been send to the registered email address'
            session['loggedin'] = True
            session['email1'] = request.form['enterEmail']
            session['otp'] = Security.generateHash(otp)
            return redirect(url_for('verifyotp'))     
    return render_template('forgotpassword.html', error=error, message=message)

@app.route('/verifyotp', methods=['POST', 'GET'])
def verifyotp():
    error = ""
    message = ""

    if 'otp' not in session:
        return render_template('forgotpassword.html', error=error, message=message)

    print('is otp in session : ', 'otp' in session)

    print(session['otp'])

    if request.method == 'POST' and 'otp' in request.form:
        verifyotp = request.form['otp']
        # print('OTP : ', type(verifyotp))
        # print('session OTP : ', session['otp'])
        if Security.generateHash(verifyotp) == session['otp']:
            session.pop('otp', None)
            return redirect(url_for('changepassword')) 
        else:
            message = "Entered wrong otp, please try again"
            return render_template('verifyOtp.html', message=message)

    return render_template('verifyOtp.html')

@app.route('/changepassword', methods=['POST', 'GET'])
def changepassword():
    message = ""

    if 'email1' not in session:
        return redirect(url_for('redirect_login_signup'))

    emailId = session['email1']
    if request.method == 'POST' and 'enterpass' in request.form and 'verifyenterpass' in request.form:
        changepass = request.form['enterpass']
        verifyChangepass = request.form['verifyenterpass']

        if not re.match(r'^([A-Za-z0-9_\.@\$!]{8,20})$', changepass):
            message = 'Password should be alphanumeric and atleast contain 8 characters along with special characters.'
            return render_template('changepassword.html', message=message)
        elif changepass == verifyChangepass:
            
            result = Services.editPassword(emailId, changepass)

            if result:
                message = 'Password updated successfully'
            else:
                message = 'Error unable to update password'
            
            print(message)

            session.pop('loggedin', None) 
            session.pop('email1', None) 

            return render_template('login_signup.html',  msg=message)
        else:
            message = 'Password does not match'
        
            return render_template('changepassword.html', message=message)

    
    return render_template('changepassword.html')



if __name__ == "__main__":
    app.run(debug=True)