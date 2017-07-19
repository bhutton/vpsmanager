import modules.vps as vps
from mock import patch, MagicMock
from tests.test_vpsmanager import VpsmanagerTestCase

expect_value = {'status': 'VPS 878 Updated\n'}

class VpsmanagerNetworkTestCase(VpsmanagerTestCase):

    #@patch('modules.vps.VPS.make_call_to_vpssvr')
    def test_delete_network_interface(self):
        #mock_vps.return_value = 'VPS 878 Updated\n'
        v = vps.VPS()
        rv = v.delete_network_interface(1, 878)
        #assert v.delete_network_interface(1, 878) is 'VPS 878 Updated\n'
        self.assertDictEqual(rv.json(), expect_value)

    def test_add_device(self):
        #mock_vps.return_value = 'VPS 878 Updated\n'
        v = vps.VPS()
        rv = v.addDevice(1, 878, 0)
        #expect_value = {'status': 'VPS 878 Updated\n'}
        self.assertDictEqual(rv.json(), expect_value)
        #assert v.addDevice(1, 878, 0) is 'VPS 878 Updated\n'
