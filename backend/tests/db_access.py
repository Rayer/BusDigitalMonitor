import unittest
from utils.auth import Auth
from requests import request
from utils.db_access import SensitiveData
import json
import utils.db_access

base_api_url = 'http://ptx.transportdata.tw/MOTC/'
bus_stop_resource = 'v2/Bus/Stop/City/Taipei?$top={data_per_session}&$skip={data_start_point}&$format=JSON'
bus_station_resource = 'v2/Bus/Station/City/Taipei?$top={data_per_session}&$skip={data_start_point}&$format=JSON'
bus_route_resource = 'v2/Bus/StopOfRoute/City/Taipei?$top={data_per_session}&$skip={data_start_point}&$format=JSON'
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
        self.fill_into_db(utils.db_access.BusStopData, bus_stop_resource)

    def test_insert_station(self):
        self.fill_into_db(utils.db_access.BusStationData, bus_station_resource)

    def test_insert_route(self):
        self.fill_into_db(utils.db_access.BusRouteData, bus_route_resource)

    def fill_into_db(self, db_writer, url_resource):
        conf = configuration.copy()
        with db_writer() as db:
            db.drop_data()
            while True:
                response = request('get', get_session_url(url_resource, conf), headers=self.auth.get_auth_header())
                conf['data_start_point'] += conf['data_per_session']
                if response.content.__len__() < 5:
                    break
                content = response.content.decode('utf8')
                stops = json.loads(content)
                for stop in stops:
                    db.write_entry(stop)

                print('Current pass : {}'.format(conf['data_start_point']))
