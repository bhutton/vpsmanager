import os
import vpsmanager
import unittest
import tempfile
import modules.vps
import modules.database
import modules.user
from contextlib import contextmanager
from flask import appcontext_pushed, g
from mock import patch
import mock
from werkzeug import generate_password_hash, check_password_hash
import werkzeug

class VpsmanagerTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, vpsmanager.app.config['DATABASE'] = tempfile.mkstemp()
        vpsmanager.app.config['TESTING'] = True
        self.app = vpsmanager.app.test_client()
        with vpsmanager.app.app_context():
            vpsmanager.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(vpsmanager.app.config['DATABASE'])

    def test_homepage_unauthenticated(self):
        rv = self.app.get('/', follow_redirects=True)
        assert 'Login' in rv.data

    @contextmanager
    def user_set(app, user):
        def handler(sender, **kwargs):
            g.user = user

        with appcontext_pushed.connected_to(handler, app):
            yield

    @patch('modules.database.DB_VPS')
    @patch('werkzeug.check_password_hash')
    @patch('modules.user.User')
    def login(self, username, password, exec_function_get_user, exec_function_check_password_hash, exec_function_db):
        #username = 'bhutton'
        #password = 'mypassword'
        self.hashed_password = generate_password_hash(password)

        werkzeug.check_password_hash().check_password_hash.return_value = True
        exec_function_get_user().checkUsername.return_value = self.getUserAccount()

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

    @patch('modules.vps.VPS')
    @patch('modules.database.DB_VPS')
    def testListVM(self, exec_function_get_status, exec_function_db_mock):
        exec_function_db_mock().getVPS.return_value = ('on', 'def', 'ghi', 'jkl')
        exec_function_get_status().getStatus.return_value = "Running"

        modules.database.DB_VPS.getVPS.return_value = None
        vps = modules.vps.VPS()
        row = vps.getVPS()

        assert (len(row) > 0)

    @patch('modules.vps.VPS')
    def addVPS(self, name, description, ram, disk, bridge, password, exec_function_vps):
        rv = self.login('bhutton@abc.com','mypassword')
        rv = self.app.get('/', follow_redirects=True)
        assert 'VPS Manager' in rv.data

        # add database mock

        exec_function_vps.getVPS.return_value = 123
        exec_function_vps().createVPS.return_value = 123


        return self.app.post('/createVPS', data=dict(
            name="test",
            description="this is a test",
            ram=1,
            disk=10,
            bridge=1,
            image=1
        ), follow_redirects=True)

        #return rv

        #print (rv.data)

        #assert b'<Response streamed [200 OK]>' in rv
        #self.assertEqual(rv.code, 200)


    @mock.patch('modules.database.DB_VPS')
    def testHomepageAuthenticated(self, exec_func_db):
        modules.database.DB_VPS.getVPS.return_value = None

        rv = self.login("myusername","mypassword")
        rv = self.app.get('/', follow_redirects=True)
        assert 'VPS Manager' in rv.data

    def testLoginPage(self):
        rv = self.app.get('/Login', follow_redirects=False)
        assert 'Login' in rv.data

    @mock.patch('modules.database.DB_Users')
    def testLogin(self, exec_func_db):
        modules.database.DB_Users.getUser.return_value = None
        return self.app.post('/validateLogin', data=dict(
            username='ben@benhutton.com.au',
            password='my password'
        ), follow_redirects=True)



    def testAddUser(self):
        return self.app.post('/createUser', data=dict(
            inputName="Fred Bloggs",
            inputEmail="fred@bloggs.com",
            inputPassword="myawesomepassword"
        ), follow_redirects=True)


    def logout(self):
        return self.app.get('/Logout', follow_redirects=True)


    def test_login_logout(self):

        # Successful Login
        rv = self.login("ben@benhutton.com.au", "Lijnfe0912")
        assert 'VPS Manager' in rv.data

        # Invalid Login
        #rv = self.login('adminx@test.com', 'default')
        #assert 'Wrong Email address or Password.' in rv.data
        
        # Logout
        rv = self.logout()
        assert 'Login' in rv.data


    #@mock.patch('vpsmanager')
    def testAddVPS(self):

        # Create VPS and return ID
        self.login("ben@benhutton.com.au", "Lijnfe0912")
        rv = self.addVPS("UnitTest2", "Unit Test", "512MB", "20GB", "0", "1")

        assert rv.data >= 0, 'VPS Successfully Created'

    def testDeleteVPS(self):

        # Create VPS and return ID
        self.login("ben@benhutton.com.au", "Lijnfe0912")
        # Delete VPS created above
        #delete_cmd = "/deleteVPS?id=" + str(rv.data)
        #rv = self.app.get(delete_cmd, follow_redirects=True)
        #assert 'VPS Successfully Deleted' in rv.data


    '''
    def test_add_delete_user(self):
        rv = self.login("ben@benhutton.com.au", "Lijnfe0912")
        rv = self.add_user("Fred Bloggs","fred@bloggs.com","abc123")
        assert rv.data >= 0, 'User Added Successfully'

        delete_cmd = "/deleteUser?id=" + str(rv.data)
        rv = self.app.get(delete_cmd, follow_redirects=True)
        assert 'User Successfully Deleted' in rv.data

    def test_start_vps(self):
        rv = self.login("ben@benhutton.com.au", "Lijnfe0912")
        start_vps_cmd = "/startVPS?id=654"
        rv = self.app.get(start_vps_cmd, follow_redirects=True)
        assert 'Running' in rv.data

    def test_stop_vps(self):
        rv = self.login("ben@benhutton.com.au", "Lijnfe0912")
        stop_vps_cmd = "/stopVPS?id=654"
        rv = self.app.get(stop_vps_cmd, follow_redirects=True)
        assert 'Stopped' in rv.data

'''

if __name__ == '__main__':
    unittest.main()