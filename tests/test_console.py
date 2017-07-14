import unittest
import modules.vps as vps
from tests.test_vpsmanager import VpsmanagerTestCase

class VPSManagerConsoleTests(VpsmanagerTestCase):
    def test_restart_console(self):
        v = vps.VPS()
        v.restartConsole(878)

if __name__ == '__main__':
    unittest.main()