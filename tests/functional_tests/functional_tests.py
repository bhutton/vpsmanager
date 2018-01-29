import time
import warnings

import os, configparser
from selenium import webdriver
import unittest

dir_path = os.path.dirname(os.path.realpath(__file__))
test_config = configparser.ConfigParser()
test_config.read("{}/testing.cfg".format(dir_path))

chrome_path = test_config.get('Chrome', 'executable_path')
url = test_config.get('Chrome', 'url')


class VPSManagerFunctionalTests(unittest.TestCase):

    def setUp(self):
        # Supress - ResourceWarning: unclosed <socket.socket [closed]
        warnings.filterwarnings("ignore", category=ResourceWarning)

        options = webdriver.ChromeOptions()
        options.binary_location = chrome_path
        options.add_argument("--disable-infobars")
        options.add_argument('headless')
        options.add_argument('window-size=1200x600, chrome.verbose=true')
        self.browser = webdriver.Chrome(options=options)
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def login(self):
        self.browser.get(url)
        self.browser.get_screenshot_as_file('login screen.png')
        self.browser.find_element_by_id("username").send_keys("ben@benhutton.com.au")
        self.browser.get_screenshot_as_file('username.png')
        self.browser.find_element_by_id("password").send_keys("Lijnfe0912")
        self.browser.get_screenshot_as_file('password.png')
        self.browser.find_element_by_id("btnSignIn").click()
        self.browser.get_screenshot_as_file('click.png')

    def get_page(self, url):
        self.browser.get(url)
        time.sleep(1)
        return self.browser.title

    def get_page_with_status(self, url):
        self.browser.get(url)
        time.sleep(1)
        return self.browser.status_code

    def test_login_page(self):
        assert 'Login - VPS Manager' in self.get_page(url)

    def test_login(self):
        self.login()
        assert 'VPS Manager' in self.browser.title
        self.browser.close()

    def test_view_vps(self):
        self.login()
        assert 'View VPS' in self.get_page(url + '/viewVPS?id=878')

    def test_create_vps(self):
        self.login()
        assert 'Add VPS' in self.get_page(url + '/AddVPS')

        self.browser.find_element_by_id('name').send_keys('test')
        self.browser.save_screenshot('add vps - name.png')

        self.browser.find_element_by_id('description').send_keys('test')
        self.browser.save_screenshot('add vps - description.png')

        return_value = self.browser.find_element_by_id('btnCreateVPS').click()
        # return_value = self.browser.current_url
        self.assertEqual(200, return_value)

    def test_modify_vps(self):
        self.login()
        assert 'Modify VPS' in self.get_page(url + '/modifyVPS?id=878')

    # def test_update_vps(self):
    #     self.login()
    #     assert 'Modify VPS' in self.get_page(url + '/modifyVPS?id=878')
    #     self.browser.find_element_by_id('btnUpdateVPS').click()
    #     # assert 'Machine Updated' in self.browser.title
    #     self.assertTrue(self.browser.find_element_by_id('success'))


    def test_click_view_vps(self):
        self.login()
        self.get_page(url)
        self.browser.find_element_by_id('878').click()
        assert 'View VPS' in self.browser.title

    def test_click_modify_vps(self):
        self.login()
        self.get_page(url)
        self.browser.find_element_by_link_text('edit').click()
        assert 'Modify VPS' in self.browser.title
        self.browser.find_element_by_id('description').clear()
        self.browser.find_element_by_id('description').send_keys('sometext')
        self.browser.find_element_by_id('btnUpdateVPS').click()
        self.browser.find_element_by_class_name('success')
        assert 'sometext' in self.browser.find_element_by_id('description').get_attribute('value')

    def test_click_user_management(self):
        self.login()
        self.get_page(url)
        self.browser.find_element_by_link_text('User Management').click()
        assert 'User Management' in self.browser.title

    def test_modify_user(self):
        self.login()
        self.get_page(url + '/UserManagement')
        self.browser.find_element_by_link_text('edit').click()
        assert 'Modify User' in self.browser.title

    def test_modify_update_user(self):
        self.login()
        self.get_page(url + '/UserManagement')
        self.browser.find_element_by_link_text('edit').click()
        assert 'Modify User' in self.browser.title

        self.browser.find_element_by_id('btnUpdateUser').click()
        success_message = self.browser.find_element_by_class_name("success").text
        assert 'User Updated Successfully' in success_message

    def test_create_user(self):
        self.login()
        self.get_page(url + '/UserManagement')
        self.browser.find_element_by_id('lnkAddUser').click()
        assert 'Add User' in self.browser.title

    def test_start_vps(self):
        self.login()
        self.get_page(url + '/startVPS?id=878')
        status = self.browser.find_element_by_id('status').text
        assert 'Running' in status

    def test_stop_vps(self):
        self.login()
        self.get_page(url + '/stopVPS?id=878')
        status = self.browser.find_element_by_id('status').text
        assert 'Stopped' in status


if __name__ == '__main__':
    unittest.main()