import os
import tempfile
from selenium import webdriver
import vpsmanager
import unittest
#from flask_testing import LiveServerTestCase

class VPSManagerFunctionalTests(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def login(self):
        self.browser.get('http://localhost:3000')
        self.browser.find_element_by_id("username").send_keys("ben@benhutton.com.au")
        self.browser.find_element_by_id("password").send_keys("Lijnfe0912")
        self.browser.find_element_by_id("btnSignIn").click()

    def test_login_page(self):
        self.browser.get('http://localhost:3000')
        assert 'Login - VPS Manager' in self.browser.title

    def test_login(self):
        self.login()
        assert 'VPS Manager' in self.browser.title

    def test_view_vps(self):
        self.login()
        self.browser.get('http://localhost:3000/viewVPS?id=878')
        assert 'View VPS' in self.browser.title

if __name__ == '__main__':
    unittest.main()