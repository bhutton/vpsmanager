import unittest
from mock import patch
import modules.vps



class TestConnectivityToVPSServer(unittest.TestCase):

    @patch('flaskext.mysql.MySQL.connect')
    def setUp(self, db_connect):
        db_connect.return_value.connect.return_value = None
        self.v = modules.vps.VPS()

    def test_make_call_to_vpssvr(self):
        assert self.v.make_call_to_vpssvr('/vpssvr/api/v1.0/tasks/statustest/1').status_code == 200


if __name__ == '__main__':
    unittest.main()
