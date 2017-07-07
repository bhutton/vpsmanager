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

    def get_page(self, url):
        self.browser.get(url)
        return self.browser.title

    def test_login_page(self):
        assert 'Login - VPS Manager' in self.get_page('http://localhost:3000')

    def test_login(self):
        self.login()
        assert 'VPS Manager' in self.browser.title

    def test_view_vps(self):
        self.login()
        assert 'View VPS' in self.get_page('http://localhost:3000/viewVPS?id=878')

    def test_create_vps(self):
        self.login()
        assert 'Add VPS' in self.get_page('http://localhost:3000/AddVPS')

    def test_modify_vps(self):
        self.login()
        assert 'Modify VPS' in self.get_page('http://localhost:3000/modifyVPS?id=878')

    def test_click_view_vps(self):
        self.login()
        self.get_page('http://localhost:3000')
        self.browser.find_element_by_id('878').click()
        assert 'View VPS' in self.browser.title

    def test_click_modify_vps(self):
        self.login()
        self.get_page('http://localhost:3000')
        self.browser.find_element_by_link_text('edit').click()
        assert 'Modify VPS' in self.browser.title

    def test_click_user_management(self):
        self.login()
        self.get_page('http://localhost:3000')
        self.browser.find_element_by_link_text('User Management').click()
        assert 'User Management' in self.browser.title

    def test_modify_user(self):
        self.login()
        self.get_page('http://localhost:3000/UserManagement')
        self.browser.find_element_by_link_text('edit').click()
        assert 'Modify User' in self.browser.title

    def test_modify_update_user(self):
        self.login()
        self.get_page('http://localhost:3000/UserManagement')
        self.browser.find_element_by_link_text('edit').click()
        assert 'Modify User' in self.browser.title
        self.browser.find_element_by_id('btnUpdateUser').click()
        success_message = self.browser.find_element_by_class_name("success").text
        assert 'User Updated Successfully' in success_message


if __name__ == '__main__':
    unittest.main()