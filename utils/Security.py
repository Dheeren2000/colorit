from cryptography.fernet import Fernet
from utils.confidential.Secrets import key
import hashlib
import time

class Security:
    
    @staticmethod 
    def encryptData(message):
        """
        Method to encrypt the given message 
        """
        fernet = Fernet(key)
        # print(f'Message : {message}')
        # print(f'Message Encode : {message.encode()}')

        cipher = fernet.encrypt(message.encode())
        return cipher.decode()

    @staticmethod 
    def dcryptData(cipher):
        """
        Method to decrypt the given cipher text
        """
        fernet = Fernet(key)
        # print(f'Cipher : {cipher}')
        # print(f'len Cipher : {len(cipher)}')

        message = fernet.decrypt(cipher.encode())

        # print(f'message : {message}')
        # print(f'message decode: {message.decode()}')
        return message.decode()


    @staticmethod
    def generateHash(message):
        """
        Method to return the Hash value of the given string using SHA256
        """
        message = message.encode('utf-8')
        return hashlib.sha256(message).hexdigest()
        


if __name__ == "__main__":

    print('Start Encrypting')
    password = "navneet@123"
    start = time.time()
    cipher = Security.encryptData(password)
    print(cipher)
    end = time.time()
    

    temp = end-start
    print(f'Total Time in Seconds : {temp} sec')
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    print('Total Time Taken : ')
    print('HH:MM:SS => %d:%d:%d' %(hours, minutes, seconds))

    print('done Encrypting')


    print('start decrypt')

    start = time.time()
    plain = Security.dcryptData(cipher)
    print(plain)
    end = time.time()
    

    temp = end-start
    print(f'Total Time in Seconds : {temp} sec')
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    print('Total Time Taken : ')
    print('HH:MM:SS => %d:%d:%d' %(hours, minutes, seconds))

    print('done decrpt')

    print('--------------------------------------------------------')
    print("Hashing : ")

    message = '897562'

    print(Security.generateHash(message))