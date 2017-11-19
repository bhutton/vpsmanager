import unittest
import modules.database.database as database
import modules.user as user
from mock import patch
from tests.test_vpsmanager import VpsmanagerTestCase

class VPSManagerUserTests(VpsmanagerTestCase):

    @patch('modules.database.database.DB_Users')
    def addUser(self, username, email, password, exec_func_user):
        database.DB_Users().createUser.return_value = 1
        return self.app.post('/createUser', data=dict(
            inputName=username,
            inputEmail=email,
            inputPassword=password
        ), follow_redirects=True)

    def test_get_users(self):
        u = user.User()
        rv = self.addUser("Fred Bloggs", "fred@bloggs.com", "abc123")
        users = u.getUsers()
        assert users != 'error running query'

    def test_get_user(self):
        u = user.User()
        rv = self.addUser("Fred Bloggs", "fred@bloggs.com", "abc123")
        users = u.getUserByEmail('ben@benhutton.com.au')
        assert users[0] != None

    def test_add_delete_user(self):
        rv = self.login("username", "password")
        rv = self.addUser("Fred Bloggs","fred@bloggs.com","abc123")
        assert len(rv.data) > 0, 'User Added Successfully'

    def test_update_user(self):
        u = user.User()
        rv = u.updateUser(21,'fred bloggs1','test1@email.com','abc1234')
        assert rv == "update successful"
        rv = u.updateUser(21, 'fred bloggs2', 'test@email.com', 'abc123')
        assert rv == "update successful"

    @patch('modules.database.database.DB_Users')
    def testDeleteUser(self, exec_func_db):
        database.DB_Users().deleteUser.return_value = ""

        rv = self.login("username", "password")
        rv = self.addUser("Fred Bloggs", "fred@bloggs.com", "abc123")
        delete_cmd = "/deleteUser?id=" + str(int(rv.data))
        rv = self.app.get(delete_cmd, follow_redirects=True)
        assert b'User Successfully Deleted' in rv.data

    def test_login_logout(self):
        # Successful Login
        rv = self.login("username", "password")
        assert b'VPS Manager' in rv.data

        # Invalid Login
        rv = self.login('adminx@test.com', 'default')
        assert b'Invalid Username or Password' in rv.data

        # Logout
        rv = self.logout()
        assert b'Login' in rv.data

    def testLoginPage(self):
        rv = self.app.get('/Login', follow_redirects=False)
        assert b'Login' in rv.data

    @patch('modules.database.database.DB_VPS')
    def testHomepageAuthenticated(self, exec_func_db):
        database.DB_VPS.getVPS.return_value = None
        rv = self.login("myusername", "mypassword")
        rv = self.app.get('/', follow_redirects=True)
        assert b'VPS Manager' in rv.data

    def test_homepage_unauthenticated(self):
        rv = self.app.get('/', follow_redirects=True)
        assert b'Login' in rv.data

    @patch('modules.database.database.DB_Users')
    def testLogin(self, exec_func_db):
        return self.app.post('/validateLogin', data=dict(
            username='usernmae',
            password='password'
        ), follow_redirects=True)


if __name__ == '__main__':
    unittest.main()