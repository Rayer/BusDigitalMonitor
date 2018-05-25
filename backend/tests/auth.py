import unittest
import utils.auth
import db_access
from requests import request
from pprint import pprint


class AuthSanity(unittest.TestCase):
    def test_auth_get_data(self):
        auth = utils.auth.Auth()
        with db_access.Sensitive_Data() as sd:
            app_id = sd.get('app_id_l1')
            app_key = sd.get('app_key_l1')

        auth.init(app_id, app_key)
        response = request('get', 'http://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei?$top=30&$format=JSON', headers=auth.get_auth_header())
        self.assertEqual(response.status_code, 200)
