import os
import vpsmanager
import unittest
import tempfile
import modules.vps as vps
import modules.database
import modules.user as user
import modules.graph
import json
from contextlib import contextmanager
from flask import appcontext_pushed, g
from mock import patch
from werkzeug import generate_password_hash

class VPSManagerUserTests(unittest.TestCase):
    def test_update_user(self):
        u = user.User()
        rv = u.updateUser(21,'fred bloggs1','test1@email.com','abc1234')
        assert rv == "update successful"
        rv = u.updateUser(21, 'fred bloggs2', 'test@email.com', 'abc123')
        assert rv == "update successful"

if __name__ == '__main__':
    unittest.main()