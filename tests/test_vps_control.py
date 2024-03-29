import unittest
import modules.vps as vps
import modules.database
import modules.graph as graph
from flask import json
from mock import patch, MagicMock
from tests.test_vpsmanager import VpsmanagerTestCase


class testControlVPS(VpsmanagerTestCase):

    @patch('modules.vps.VPS')
    def test_start_vps(self, exec_func_vps):
        self.login("username", "password")
        start_vps_cmd = "/startVPS?id=654"

        modules.vps.VPS().ctrlVPS.return_value = "Started VPS 123"
        modules.vps.VPS().getIndVPS.return_value = self.getVPSData()

        rv = self.app.get(start_vps_cmd, follow_redirects=True)
        assert b'/stopVPS' in rv.data

    @patch('modules.graph.GraphTraffic')
    @patch('modules.vps.VPS')
    def test_stop_vps(self, exec_func_vps, exec_func_graph):
        modules.graph.GraphTraffic().return_value = "abc.txt"
        rv = self.login("username", "password")

        stop_vps_cmd = "/stopVPS?id=654"
        rv = self.app.get(stop_vps_cmd, follow_redirects=True)
        assert b'View VPS' in rv.data

    def testListVM(self):
        vps = modules.vps.VPS()
        row = vps.getVPS()

        assert (len(row) > 0)

    def testAddVPS(self):
        self.login("username", "password")
        rv = self.addVPS("UnitTest2", "Unit Test", "512MB", "20GB", "0", "1")
        assert b'VPS Successfully Created' in rv.data

    def testModifyVPS(self):
        self.login("username", "password")
        rv = self.modifyVPS("UnitTest2", "Unit Test", "512MB", "20GB", "0", "1")
        assert b'878' in rv.data

    @patch('modules.vps.VPS')
    def addVPS(self, name, description, ram, disk, bridge, password, exec_function_vps):
        rv = self.login('bhutton@abc.com', 'mypassword')
        rv = self.app.get('/', follow_redirects=True)
        assert b'VPS Manager' in rv.data

        exec_function_vps.getVPS.return_value = "VPS Successfully Created"
        exec_function_vps().createVPS.return_value = "VPS Successfully Created"

        return self.app.post('/createVPS', data=dict(
            name="test",
            description="this is a test",
            ram=1,
            disk=10,
            bridge=1,
            image=1
        ), follow_redirects=True)

    @patch('modules.vps.VPS')
    def modifyVPS(self, name, description, ram, disk, bridge, password, exec_function_vps):
        rv = self.login('bhutton@abc.com', 'mypassword')
        rv = self.app.get('/', follow_redirects=True)

        exec_function_vps.getVPS.return_value = "VPS Successfully Updated"
        exec_function_vps().updateVPS.return_value = "Machine successfully updated"

        return_value = self.app.post('/updateVPS', data=dict(
            id=878,
            name="test",
            description="this is a test",
            ram=1,
            disk=10,
            bridge=1,
            image=1,
            path="",
            startscript = "",
            stopscript = ""
        ), follow_redirects=True)

        return return_value

    @patch('modules.vps.VPS')
    def testDeleteVPS(self, exec_function_vps):
        exec_function_vps().delVPS.return_value = "success", "VPS Successfully Deleted"

        self.login("username", "password")
        rv = self.addVPS("UnitTest2", "Unit Test", "512MB", "20GB", "0", "1")

        delete_cmd = "/deleteVPS?id=" + str(rv.data)
        rv = self.app.get(delete_cmd, follow_redirects=True)
        assert b'VPS Successfully Deleted' in rv.data

    @patch('modules.vps.VPS')
    def test_get_vps_status(self, mock_vps):
        expect_value = {'status': 'Stopped'}
        modules.vps.VPS().getStatus().json.return_value = expect_value
        v = vps.VPS()

        status = v.getStatus(878).json()
        assert 'Stopped' in status['status']

    def test_graph(self):
        g = graph.GraphTraffic()



if __name__ == '__main__':
    unittest.main()