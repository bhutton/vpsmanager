from flask import json

import modules
import modules.vps as vps
from tests.test_vpsmanager import VpsmanagerTestCase
from mock import patch, MagicMock
import modules.vps as vps

class VpsmanagerNetworkTestCase(VpsmanagerTestCase):

    expect_value = {'status': 'VPS 878 Updated\n'}

    @patch('modules.vps.VPS')
    def test_delete_network_interface(self, mock_vps):
        modules.vps.VPS().delete_network_interface().json.return_value = self.expect_value
        v = vps.VPS()
        rv = v.delete_network_interface(1, 878)
        self.assertDictEqual(rv.json(), self.expect_value)

    @patch('modules.vps.VPS')
    def test_add_device(self, mock_vps):
        modules.vps.VPS().addDevice().json.return_value = self.expect_value
        v = vps.VPS()
        rv = v.addDevice(1, 878, 0)
        self.assertDictEqual(rv.json(), self.expect_value)
