import unittest
import modules.vps as vps
from mock import patch


class MyTestCase(unittest.TestCase):

    @patch('modules.database.DB_VPS')
    def test_test_api_call(self, exec_function_db):
        exec_function_db.return_value = None
        v = vps.VPS()
        v.rest_api_call()



if __name__ == '__main__':
    unittest.main()
