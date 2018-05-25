import unittest
from utils.auth import Auth
from requests import request
from utils.db_access import SensitiveData
import json

base_api_url = 'http://ptx.transportdata.tw/MOTC/'
bus_stop_resource = 'v2/Bus/Stop/City/Taipei?$top={data_per_session}&$skip={data_start_point}&$format=JSON'
configuration = {'data_per_session': 1000, 'data_start_point': 0}


def get_session_url(conf):
    return base_api_url + bus_stop_resource.format(**conf)


class DBInsertUpdateTest(unittest.TestCase):
    def test_db_insert_update(self):

        auth = Auth()
        with SensitiveData() as sd:
            app_id = sd.get('app_id_l1')
            app_key = sd.get('app_key_l1')

        auth.init(app_id, app_key)

        conf = configuration.copy()
        while True:
            response = request('get', get_session_url(conf), headers=auth.get_auth_header())
            conf['data_start_point'] += conf['data_per_session']
            if response.content.__len__() < 5:
                break
            content = response.content.decode('utf8')
            bus_stops = json.loads(content)

            print('Current pass : {}'.format(conf['data_start_point']))

