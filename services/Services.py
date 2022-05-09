# Service class to provide the services to the client
from ast import expr_context
import psycopg2
from models.ImageData import ImageData
from models.User import User
from postgres.ConnectionManager import ConnectionManager


class Services:

    # method to login the user if exists
    @staticmethod
    def loginService(emailId, password):

        conn = ConnectionManager().getConnection()

        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('SELECT * FROM app_users WHERE email=%s and password=%s',(emailId, password))
            result = cursor.fetchone()
        except:
            print("Exception occured in loginService")

        if result is None:
            return None

        return User(result['fname'], result['lname'], result['email'], id=result['id'])

    # method to check if the given user exists or not usin email
    @staticmethod 
    def isUserExits(emailId):
        conn = ConnectionManager().getConnection()

        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('SELECT * FROM app_users WHERE email=%s',(emailId,))
            result = cursor.fetchone()
        except:
            print("Exception occured in isUserExits")

        if result is None:
            return None

        return User(result['fname'], result['lname'], result['email'], id=result['id'], password=result['password'])

    # method to register the user 
    @staticmethod
    def registerService(user):
        conn = ConnectionManager().getConnection()

        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('INSERT INTO app_users (fname,lname,email,password) VALUES (%s, %s, %s, %s)', 
            (user.firstName, user.lastName, user.email, user.password, ))
            conn.commit()

            return True
        except:
            print("Exception occured in registerService")
            return False


    # method to insert the image into the db
    @staticmethod
    def insertImage(user:User, imageData:ImageData):
        conn = ConnectionManager().getConnection()

        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('INSERT INTO imagedata (grayImage, rgbImage, fileName, userId, uniqueId) VALUES(%s,%s,%s,%s,%s)', 
                            (psycopg2.Binary(imageData.grayImage), 
                            psycopg2.Binary(imageData.rgbImage), 
                            imageData.fileName, 
                            user.id, 
                            imageData.uniqueId))
            conn.commit()

            return True
        except:
            print("Exception occured in insertImage")
            return False

    # method to get the ImageData by the unqiue id 
    @staticmethod
    def getImageDataByUniqueId(uniqueId):
        conn = ConnectionManager().getConnection()

        try:
             # fetching the image data from the DB
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('SELECT * FROM imagedata WHERE uniqueId = %s',(uniqueId,))
            imageData = cursor.fetchone()


            if imageData is None:
                return None
            else:
                return ImageData(fileName=imageData[3], 
                                grayImage=imageData[1], 
                                rgbImage=imageData[2], 
                                uniqueId=imageData[6], 
                                datetime=imageData[5], 
                                id=imageData[0])

        except:
            print("Excpetion occured in getImageDataByUniqueID")
            return None



    # method to get all the images of user 
    def getUserImages(searchName, userId, limit, offset):
        
        conn = ConnectionManager().getConnection()

        commonCountQuery = "SELECT COUNT(*) FROM imagedata WHERE userid = %(uid)s"
        commonImageDataQuery = "SELECT fileName, grayImage, rgbImage, uniqueId, to_char(datetime, 'DD Mon YYYY, HH:MI AM') FROM ImageData WHERE userid = %(uid)s"

        if searchName != 'NA':
            selectCountQuery = {
                'query': commonCountQuery + " and LOWER(imagedata.fileName) LIKE %(searchValue)s",
                'inputs': {'uid' : userId, 'searchValue': searchName.lower() + '%'}
            }

            selectImageDataQuery = {
                'query':  commonImageDataQuery + " and LOWER(filename) LIKE %(searchValue)s ORDER BY datetime DESC LIMIT %(limits)s OFFSET %(offSet)s",
                'inputs': {'uid': userId, 'searchValue': searchName.lower() + '%', 'limits': limit, 'offSet': offset}
            }

        else:

            selectCountQuery = {
                'query': commonCountQuery,
                'inputs': {'uid' : userId}
            }

            selectImageDataQuery = {
                'query':  commonImageDataQuery + " ORDER BY datetime DESC LIMIT %(limits)s OFFSET %(offSet)s",
                'inputs': {'uid': userId, 'limits': limit, 'offSet': offset}
            }

        imageDataCount = 0    
        records = None

        try:
            # fetching the count of image data from the DB
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(selectCountQuery['query'], selectCountQuery['inputs'])
            imageDataCount = cursor.fetchone()[0]

        except:
            print("Exception occured in getUserImages : imageDataCount")
            imageDataCount = 0

        # print('!NA :', imageDataCount)

        try:
            # fetching the image data from the DB
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(selectImageDataQuery['query'], selectImageDataQuery['inputs'])
            records = cursor.fetchall()

        except:
            print("Exception occured in getUserImages : records")
            records = None

        return imageDataCount, records

    # method to change the password of the user
    def editPassword(emailId, newPassword):
        conn = ConnectionManager().getConnection()
        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('UPDATE app_users SET password=%s WHERE email=%s',
                            (newPassword, emailId))
            conn.commit()
            return True
        except:
            print("Exception occured in editPassword")
            return False

    # method to delete the image form the db
    def deleteImages(uniqueId):
        conn = ConnectionManager().getConnection()

        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('DELETE FROM ImageData WHERE uniqueId = %s', (uniqueId,))
            conn.commit()        

            return True
        except:
            print("Exception occured in deleteImages")
            return False
        







