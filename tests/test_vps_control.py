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
from tests.test_vpsmanager import VpsmanagerTestCase

class testControlVPS(unittest.TestCase):
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

    @patch('modules.graph.GraphTraffic')
    @patch('modules.vps.VPS')
    def test_start_vps(self, exec_func_vps, exec_func_graph):
        modules.graph.GraphTraffic().return_value = "abc.txt"

        rv = self.login("username", "password")
        modules.vps.VPS().ctrlVPS.return_value = "Started VPS 123"
        modules.vps.VPS().getIndVPS.return_value = self.getVPSData()
        start_vps_cmd = "/startVPS?id=654"
        rv = self.app.get(start_vps_cmd, follow_redirects=True)
        assert b'/stopVPS' in rv.data

    def getVPSData(self):
        self.vpsdata = [[]]
        self.vpsdata[0].append(123)
        self.vpsdata[0].append("test")
        self.vpsdata[0].append("this is a test")
        self.vpsdata[0].append("FreeBSD")
        self.vpsdata[0].append(512)

        return self.vpsdata

    @patch('modules.graph.GraphTraffic')
    @patch('modules.vps.VPS')
    def test_stop_vps(self, exec_func_vps, exec_func_graph):
        modules.graph.GraphTraffic().return_value = "abc.txt"
        rv = self.login("username", "password")
        modules.vps.VPS().ctrlVPS.return_value = "Stopped VPS 123"
        modules.vps.VPS().getIndVPS.return_value = self.getVPSData()
        modules.vps.VPS().getStatus.return_value = "Stopped"

        stop_vps_cmd = "/stopVPS?id=654"
        rv = self.app.get(stop_vps_cmd, follow_redirects=True)
        assert b'/startVPS' in rv.data


if __name__ == '__main__':
    unittest.main()