import mysql.connector as sql
import json
application_name = 'bdm'


class SensitiveData:
    def __enter__(self):
        self.conn = sql.connect(user='apps', password='apps', database='apps')
        cursor = self.conn.cursor()
        cursor.execute('select `key`, value from app_sensitive_values where app_name = \'{}\''.format(application_name))
        result = cursor.fetchall()
        self.dict = {}
        for key, value in result:
            self.dict.update({key: value})
        cursor.close()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def get(self, name):
        return self.dict[name]


class CommonDataInterface:

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sql.connect(user='apps', password='apps', database='apps')
        return self

    def drop_data(self):
        cur = self.conn.cursor()
        cur.execute(f'delete from {self.db_name}')
        cur.close()
        self.conn.commit()

    def write_db(self, data_entry):
        keys = []
        values = []
        for k, v in data_entry.items():
            if v is not None:
                keys.append('`' + k + '`')
                values.append('\'' + str(v).replace('\'', '\\\'') + '\'')
        c = self.conn.cursor()
        key_string = ','.join(keys)
        value_string = ','.join(values)
        c.execute(f'INSERT INTO `apps`.`{self.db_name}` ({key_string}) VALUES ({value_string})')
        c.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class BusStationData(CommonDataInterface):

    def __init__(self):
        super().__init__('bmd_station')

    def write_entry(self, station_info):
        data_entry = {
            # 'authority': station_info['AuthorityID'],
            'station_uid': station_info['StationUID'],
            'station_id': station_info['StationID'],
            'station_address': station_info.get('StationAddress'),
            'name_tw': station_info['StationName'].get('Zh_tw'),
            'name_en': station_info['StationName'].get('En'),
            'latitude': station_info['StationPosition']['PositionLat'],
            'longitude': station_info['StationPosition']['PositionLon'],
            'update_time': station_info['UpdateTime'],
            'version': station_info['VersionID']
        }

        # For debugging and testing
        stop_routes = station_info.get('Stops')
        stop_route_value = []
        if stop_routes is not None:
            for stop_route in stop_routes:
                stop_route_value.append((stop_route.get('StopUID'), stop_route.get('StopID'),
                                         stop_route.get('RouteUID'), stop_route.get('RouteID'), stop_route['RouteName'].get('Zh_tw')))
        data_entry.update({'stop_routes': json.dumps(stop_route_value)})
        self.write_db(data_entry)


class BusStopData(CommonDataInterface):

    def __init__(self):
        super().__init__('bmd_station_stop')

    def write_entry(self, stop_info):
        data_entry = {
            'stop_authority': stop_info['AuthorityID'],
            'stop_uid': stop_info['StopUID'],
            'stop_id': stop_info['StopID'],
            'latitude': stop_info['StopPosition']['PositionLat'],
            'longitude': stop_info['StopPosition']['PositionLon'],
            'stop_name_zh': stop_info['StopName'].get('Zh_tw'),
            'stop_name_en': stop_info['StopName'].get('En'),
            'bearing': stop_info.get('Bearing'),
            'station_id': stop_info.get('StationID'),
            'description': stop_info.get('StopDescription'),
            'city': stop_info.get('City'),
            'city_code': stop_info.get('CityCode'),
            'location_city_code': stop_info.get('LocationCityCode'),
            'update_time': stop_info['UpdateTime'],
            'version': stop_info['VersionID']
        }
        self.write_db(data_entry)


if __name__ == '__main__':
    with SensitiveData() as data:
        id1 = data.get('app_id_l1')
        token1 = data.get('app_key_l1')
        id2 = data.get('app_id_l2')
        token2 = data.get('app_key_l2')

    print(id1, token1, id2, token2)
