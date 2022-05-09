import math 
import random

# class for OTP Generation
class OtpGenerator:

    # method to return the random 6 digit otp
    @staticmethod
    def getRandomOtp():
        ## storing strings in a list
        digits = [i for i in range(0, 10)]

        ## initializing a string
        otp = ""

        ## we can generate 6 digit random no
        for i in range(6):
            index = math.floor(random.random() * 10)

            otp += str(digits[index])

        return otp
