from selenium import webdriver
from flask_testing import LiveServerTestCase

browser = webdriver.Firefox()
browser.get('http://localhost:3000')

assert 'Login - VPS Manager' in browser.title
