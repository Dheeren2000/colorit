import unittest
import sys
import os
import glob
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.ImageUtils import ImageUtils
from services.Services import Services

class ServiceTest(unittest.TestCase):

    # to test the user existence service
    def test_userExists(self):

        testEmail = 'nav@gmail.com'

        user = Services.isUserExits(testEmail)

        self.assertEqual(user, None)

    # to test the login service
    def test_loginService(self):

        testEmail = 'nav@gmail.com'
        testPassword = 'nav@123465'

        result = Services.loginService(testEmail, testPassword)

        self.assertEqual(result, None)

    # to test the gray image detection utility 
    def test_grayImage(self):

        grayImageDir = 'test\\resources\gray\*.jpg'

        for img in glob.glob(grayImageDir):
            result = ImageUtils.isGrayImage(img)

            self.assertEqual(result, True)

    # to test the gray image detection utility 
    def test_colorImage(self):

        grayImageDir = 'test\\resources\color\*.jpg'

        for img in glob.glob(grayImageDir):
            result = ImageUtils.isGrayImage(img)

            self.assertEqual(result, False)

if __name__ == "__main__":
    unittest.main()
