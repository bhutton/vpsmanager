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

class VpsmanagerNetworkTestCase(unittest.TestCase):
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

    @patch('modules.vps.VPS.make_call_to_vpssvr')
    def test_delete_network_interface(self, mock_vps):
        mock_vps.return_value = 'VPS 878 Updated\n'
        v = vps.VPS()
        assert v.delete_network_interface(1, 878) is 'VPS 878 Updated\n'

    def test_add_device(self):
        v = vps.VPS()
        rv = v.addDevice(1, 878, 0)
        expect_value = {'status': 'VPS 878 Updated\n'}
        self.assertDictEqual(rv.json(), expect_value)
