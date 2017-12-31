import time
import warnings

import os, configparser
from selenium import webdriver
import unittest

dir_path = os.path.dirname(os.path.realpath(__file__))
test_config = configparser.ConfigParser()
test_config.read("{}/testing.cfg".format(dir_path))

chrome_path = test_config.get('Chrome', 'executable_path')


class VPSManagerFunctionalTests(unittest.TestCase):

    def setUp(self):
        # Supress - ResourceWarning: unclosed <socket.socket [closed]
        warnings.filterwarnings("ignore", category=ResourceWarning)

        options = webdriver.ChromeOptions()
        options.binary_location = chrome_path
        options.add_argument('headless')
        options.add_argument('window-size=1200x600, chrome.verbose=true')
        self.browser = webdriver.Chrome(options=options)
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def login(self):
        self.browser.get('http://localhost:3000')
        self.browser.get_screenshot_as_file('login screen.png')
        self.browser.find_element_by_id("username").send_keys("ben@benhutton.com.au")
        self.browser.get_screenshot_as_file('username.png')
        self.browser.find_element_by_id("password").send_keys("Lijnfe0912")
        self.browser.find_element_by_id("btnSignIn").click()

    def get_page(self, url):
        self.browser.get(url)
        #time.sleep(1)
        return self.browser.title

    def test_login_page(self):
        assert 'Login - VPS Manager' in self.get_page('http://localhost:3000')

    def test_login(self):
        self.login()
        assert 'VPS Manager' in self.browser.title
        self.browser.close()

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

    def test_create_user(self):
        self.login()
        self.get_page('http://localhost:3000/UserManagement')
        self.browser.find_element_by_id('lnkAddUser').click()
        assert 'Add User' in self.browser.title

if __name__ == '__main__':
    unittest.main()