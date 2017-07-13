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

class VPSManagerConsoleTests(unittest.TestCase):
    def test_restart_console(self):
        v = vps.VPS()
        v.restartConsole(878)

if __name__ == '__main__':
    unittest.main()