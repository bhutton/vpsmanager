from selenium import webdriver
from flask_testing import LiveServerTestCase

class VPSManagerFunctionalTests(LiveServerTestCase):

    def test_home_page(self):
        browser = webdriver.Firefox()
        browser.get('http://localhost:3000')

        assert 'Login - VPS Manager' in browser.title
        browser.quit()

if __name__ == '__main__':
    unittest.main()