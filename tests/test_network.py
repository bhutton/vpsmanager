from flask import json

import modules.vps as vps
from mock import patch, MagicMock
from tests.test_vpsmanager import VpsmanagerTestCase

class VpsmanagerNetworkTestCase(VpsmanagerTestCase):

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
