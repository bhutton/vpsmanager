import unittest
from mock import patch
import modules.vps

'''
Note: These tests require the vpsserver.py server to 
be started from within the vpssvr server app.

The configuration settings in "configuration.cfg" under
[vps_server] must be set to connect to the relevant
server.
'''


class TestConnectivityToVPSServer(unittest.TestCase):

    @patch('flaskext.mysql.MySQL.connect')
    def setUp(self, db_connect):
        db_connect.return_value.connect.return_value = None
        self.v = modules.vps.VPS()

    def test_make_teststatus_call_to_vpssvr(self):
        assert self.v.make_call_to_vpssvr('/vpssvr/api/v1.0/tasks/statustest/1').status_code == 200

    def test_make_invalid_call(self):
        assert self.v.make_call_to_vpssvr('/vpssvr/api/v1.0/tasks/statu/1').status_code == 404


if __name__ == '__main__':
    unittest.main()
