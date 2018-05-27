import unittest
from utils.auth import Auth
from requests import request
from utils.db_access import SensitiveData
import json
import utils.db_access

base_api_url = 'http://ptx.transportdata.tw/MOTC/'
bus_stop_resource = 'v2/Bus/Stop/City/Taipei?$top={data_per_session}&$skip={data_start_point}&$format=JSON'
bus_station_resource = 'v2/Bus/Station/City/Taipei?$top={data_per_session}&$skip={data_start_point}&$format=JSON'
configuration = {'data_per_session': 1000, 'data_start_point': 0}


def get_session_url(func_url, conf):
    return base_api_url + func_url.format(**conf)


class DBInsertStopData(unittest.TestCase):

    def setUp(self):
        self.auth = Auth()
        with SensitiveData() as sd:
            app_id = sd.get('app_id_l1')
            app_key = sd.get('app_key_l1')

        self.auth.init(app_id, app_key)

    def test_insert_stop(self):

        conf = configuration.copy()
        with utils.db_access.BusStopData() as bsd:
            bsd.drop_data()
            while True:
                response = request('get', get_session_url(bus_stop_resource, conf), headers=self.auth.get_auth_header())
                conf['data_start_point'] += conf['data_per_session']
                if response.content.__len__() < 5:
                    break
                content = response.content.decode('utf8')
                stops = json.loads(content)
                for stop in stops:
                    bsd.write_entry(stop)

                print('Current pass : {}'.format(conf['data_start_point']))

    def test_insert_station(self):

        conf = configuration.copy()
        with utils.db_access.BusStationData() as bsd:
            bsd.drop_data()
            while True:
                response = request('get', get_session_url(bus_station_resource, conf), headers=self.auth.get_auth_header())
                conf['data_start_point'] += conf['data_per_session']
                if response.content.__len__() < 5:
                    break
                content = response.content.decode('utf8')
                stops = json.loads(content)
                for stop in stops:
                    bsd.write_entry(stop)

                print('Current pass : {}'.format(conf['data_start_point']))