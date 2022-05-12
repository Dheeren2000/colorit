import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.Security import Security

class SecurityTest(unittest.TestCase):
    
    
    def test_encryption(self):
        msg1 = "THis is test meassage"
        msg2 = "This is test meassage"
        cipher1 = Security.encryptData(msg1)
        cipher2 = Security.encryptData(msg2)

        self.assertNotEqual(cipher1, cipher2)


    def test_decryption(self):
        msg1 = "THis is test meassage"
        msg2 = "This is test meassage"

        cipher1 = Security.encryptData(msg1)
        cipher2 = Security.encryptData(msg2)


        plainText1 = Security.dcryptData(cipher1)
        plainText2 = Security.dcryptData(cipher2)

        self.assertNotEqual(plainText1, plainText2)
    

if __name__ == '__main__':
    unittest.main()


