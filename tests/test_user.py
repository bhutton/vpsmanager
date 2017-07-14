import os
import vpsmanager
import unittest
import tempfile
import modules.vps as vps
import modules.database
import modules.user as user
import modules.graph
import json
from contextlib import contextmanager
from flask import appcontext_pushed, g
from mock import patch
from werkzeug import generate_password_hash

class VPSManagerUserTests(unittest.TestCase):
    def setUp(self):
        self.db_fd, vpsmanager.app.config['DATABASE'] = tempfile.mkstemp()
        vpsmanager.app.config['TESTING'] = True
        self.app = vpsmanager.app.test_client()
        with vpsmanager.app.app_context():
            vpsmanager.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(vpsmanager.app.config['DATABASE'])

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

    @patch('modules.database.DB_Users')
    def addUser(self, username, email, password, exec_func_user):
        modules.database.DB_Users().createUser.return_value = 1
        return self.app.post('/createUser', data=dict(
            inputName=username,
            inputEmail=email,
            inputPassword=password
        ), follow_redirects=True)

    def test_update_user(self):
        u = user.User()
        rv = u.updateUser(21,'fred bloggs1','test1@email.com','abc1234')
        assert rv == "update successful"
        rv = u.updateUser(21, 'fred bloggs2', 'test@email.com', 'abc123')
        assert rv == "update successful"

    def test_add_delete_user(self):
        rv = self.login("username", "password")
        rv = self.addUser("Fred Bloggs","fred@bloggs.com","abc123")
        assert len(rv.data) > 0, 'User Added Successfully'

    @patch('modules.database.DB_Users')
    def testDeleteUser(self, exec_func_db):
        modules.database.DB_Users().deleteUser.return_value = ""

        rv = self.login("username", "password")
        rv = self.addUser("Fred Bloggs", "fred@bloggs.com", "abc123")
        delete_cmd = "/deleteUser?id=" + str(int(rv.data))
        rv = self.app.get(delete_cmd, follow_redirects=True)
        assert b'User Successfully Deleted' in rv.data

if __name__ == '__main__':
    unittest.main()