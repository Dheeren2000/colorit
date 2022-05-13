import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from resources.properties import driverPath, urlPath

class SeleniumTest(unittest.TestCase):
    
    # setup the chrome driver
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(driverPath))

    def test_isWebLauch(self):
        driver = self.driver
        driver.get(urlPath)
        driver.maximize_window()
        time.sleep(3)
        self.assertIn("ColorIt.io", driver.title)
        driver.close()

    def test_login_fail(self):
        driver = self.driver
        driver.get(urlPath)
        driver.maximize_window()
        time.sleep(3)
        self.assertIn("ColorIt.io", driver.title)

        loginSignupBtn = driver.find_element_by_xpath('/html/body/section/div/div/div[2]/a/button')
        loginSignupBtn.click()

        emailInput = driver.find_element_by_xpath('//*[@id="Email_login"]')
        passwordInput = driver.find_element_by_xpath('//*[@id="password_login"]')


        emailInput.send_keys('nav@gmail.com')
        passwordInput.send_keys('nav@123456')

        time.sleep(3)

        signBtn = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/button')
        signBtn.click()

        time.sleep(3)

        result = driver.find_element_by_xpath('//*[@id="container"]/div[3]/div/div[2]/div')

        print(result.text)


        self.assertEqual(result.text, 'Incorrect username / password !')

        driver.close()


    # test login success
    def test_login_success(self):

        driver = self.driver
        driver.get(urlPath)
        driver.maximize_window()
        time.sleep(3)
        self.assertIn("ColorIt.io", driver.title)

        loginSignupBtn = driver.find_element_by_xpath('/html/body/section/div/div/div[2]/a/button')
        loginSignupBtn.click()

        emailInput = driver.find_element_by_xpath('//*[@id="Email_login"]')
        passwordInput = driver.find_element_by_xpath('//*[@id="password_login"]')


        emailInput.send_keys('navneetdavang@gmail.com')
        passwordInput.send_keys('navneet@123')

        time.sleep(3)

        signBtn = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/button')
        signBtn.click()

        time.sleep(3)

        dashboardUserStatus = driver.find_element_by_xpath('/html/body/nav/div')

        result = dashboardUserStatus.text

        time.sleep(3)
        self.assertEqual(result, 'Navneet Davang')

        driver.close()


        

    # close the chrome driver
    def closeBrowser(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()