import modules.vps as vps
from mock import patch, MagicMock
from tests.test_vpsmanager import VpsmanagerTestCase



class VpsmanagerNetworkTestCase(VpsmanagerTestCase):

    expect_value = {'status': 'VPS 878 Updated\n'}

    def test_delete_network_interface(self):
        v = vps.VPS()
        rv = v.delete_network_interface(1, 878)
        self.assertDictEqual(rv.json(), self.expect_value)

    def test_add_device(self):
        v = vps.VPS()
        rv = v.addDevice(1, 878, 0)
        self.assertDictEqual(rv.json(), self.expect_value)
