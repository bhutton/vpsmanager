import os
import vpsmanager
import unittest
import tempfile
from contextlib import contextmanager
from flask import appcontext_pushed, g
from mock import patch
from werkzeug import generate_password_hash

class VpsmanagerTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, vpsmanager.app.config['DATABASE'] = tempfile.mkstemp()
        vpsmanager.app.config['TESTING'] = True
        self.app = vpsmanager.app.test_client()
        with vpsmanager.app.app_context():
            vpsmanager.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(vpsmanager.app.config['DATABASE'])

    @contextmanager
    def user_set(app, user):
        def handler(sender, **kwargs):
            g.user = user

        with appcontext_pushed.connected_to(handler, app):
            yield

    @patch('modules.user.User')
    def login(self,
              username,
              password,
              exec_function_get_user):
        self.hashed_password = generate_password_hash(password)

        if (username == "username" and password == "password"):
            exec_function_get_user().checkUsername.return_value \
                = self.getUserAccount()

        return self.app.post('/validateLogin', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def getUserAccount(self):
        self.userdata = [[]]
        self.userdata[0].append("bhutton")
        self.userdata[0].append("def")
        self.userdata[0].append("ghi")
        self.userdata[0].append(self.hashed_password)

        return self.userdata

    def getVPSData(self):
        self.vpsdata = [[]]
        self.vpsdata[0].append(123)
        self.vpsdata[0].append("test")
        self.vpsdata[0].append("this is a test")
        self.vpsdata[0].append("FreeBSD")
        self.vpsdata[0].append(512)

        return self.vpsdata


    def logout(self):
        return self.app.get('/Logout', follow_redirects=True)

    def getVPSData(self):
        self.vpsdata = [[]]
        self.vpsdata[0].append(123)
        self.vpsdata[0].append("test")
        self.vpsdata[0].append("this is a test")
        self.vpsdata[0].append("FreeBSD")
        self.vpsdata[0].append(512)

        return self.vpsdata

if __name__ == '__main__':
    unittest.main()