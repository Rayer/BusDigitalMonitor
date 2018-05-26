import mysql.connector as sql

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


class BusStationData:
    def __enter__(self):
        self.conn = sql.connect(user='apps', password='apps', database='apps')

    def insert_station_data(self, station_info):
        data_entry = {
            'authority': station_info['AuthorityID'],
            'station_uid': station_info['StopUID'],
            'station_id': station_info['StopID'],
            'station_position': station_info[''],
            'station_address': station_info[''],
        }

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class BusStopData:
    def __enter__(self):
        self.conn = sql.connect(user='apps', password='apps', database='apps')
        return self

    def write_stop_info(self, stop_info):
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
            'location_city_code': stop_info.get('LocationCityCode')
        }
        keys = []
        values = []
        for k, v in data_entry.items():
            if v is not None:
                keys.append('`' + k + '`')
                values.append('\'' + str(v).replace('\'', '\\\'') + '\'')

        c = self.conn.cursor()
        key_string = ','.join(keys)
        value_string = ','.join(values)
        # print(f'INSERT INTO `apps`.`bmd_station_stop` ({key_string}) VALUES ({value_string})')
        c.execute(f'INSERT INTO `apps`.`bmd_station_stop` ({key_string}) VALUES ({value_string})')
        c.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    with SensitiveData() as data:
        id1 = data.get('app_id_l1')
        token1 = data.get('app_key_l1')
        id2 = data.get('app_id_l2')
        token2 = data.get('app_key_l2')

    print(id1, token1, id2, token2)
