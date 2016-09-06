import os
import vpsmanager
import unittest
import tempfile

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

    def test_homepage_authenticated(self):
        rv = self.login("ben@benhutton.com.au", "Lijnfe0912")
        rv = self.app.get('/', follow_redirects=True)
        assert 'VPS Manager' in rv.data

    def test_login_page(self):
        rv = self.app.get('/Login', follow_redirects=False)
        assert 'Login' in rv.data

    def add_vps(self, name, description, ram, disk, bridge):
        return self.app.post('/createVPS', data=dict(
            name=name,
            description=description,
            ram=ram,
            disk=disk,
            bridge=bridge
        ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/validateLogin', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def add_user(self, username, email, password):
        return self.app.post('/createUser', data=dict(
            inputName=username,
            inputEmail=email,
            inputPassword=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/Logout', follow_redirects=True)

    def test_login_logout(self):

        # Successful Login
        rv = self.login("ben@benhutton.com.au", "Lijnfe0912")
        assert 'VPS Manager' in rv.data

        # Invalid Login
        rv = self.login('adminx@test.com', 'default')
        assert 'Wrong Email address or Password.' in rv.data
        
        # Logout
        rv = self.logout()
        assert 'Login' in rv.data

    def test_add_delete_vps(self):

        # Create VPS and return ID
        rv = self.login("ben@benhutton.com.au", "Lijnfe0912")
        rv = self.add_vps("UnitTest2","Unit Test","512MB","20GB","0")
        assert rv.data >= 0, 'VPS Successfully Created'

        # Delete VPS created above
        delete_cmd = "/deleteVPS?id=" + str(rv.data)
        rv = self.app.get(delete_cmd, follow_redirects=True)
        assert 'VPS Successfully Deleted' in rv.data

    def test_add_delete_user(self):

        rv = self.login("ben@benhutton.com.au", "Lijnfe0912")
        rv = self.add_user("Fred Bloggs","fred@bloggs.com","abc123")
        assert rv.data >= 0, 'User Added Successfully'

        delete_cmd = "/deleteUser?id=" + str(rv.data)
        rv = self.app.get(delete_cmd, follow_redirects=True)
        assert 'User Successfully Deleted' in rv.data

    #def test_add_image(self):
    #    rv = self.login("ben@benhutton.com.au", "Lijnfe0912")
    #    rv = self.adduser("IMG01","")

        



if __name__ == '__main__':
    unittest.main()