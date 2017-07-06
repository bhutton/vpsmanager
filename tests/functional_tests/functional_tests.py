import os
import tempfile

from selenium import webdriver
import vpsmanager
import unittest
#from flask_testing import LiveServerTestCase

class VPSManagerFunctionalTests(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    #def tearDown(self):
    #    os.close(self.db_fd)
    #    os.unlink(vpsmanager.app.config['DATABASE'])

    def test_login_page(self):
        self.browser.get('http://localhost:3000')
        assert 'Login - VPS Manager' in self.browser.title
        self.browser.quit()

    def test_login(self):
        self.browser.get('http://localhost:3000')
        self.browser.find_element_by_id("username").send_keys("ben@benhutton.com.au")
        self.browser.find_element_by_id("password").send_keys("Lijnfe0912")
        self.browser.find_element_by_id("btnSignIn").click()


if __name__ == '__main__':
    unittest.main()