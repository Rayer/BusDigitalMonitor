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


class BusStopInfo:
    def __enter__(self):
        self.conn = sql.connect(user='apps', password='apps', database='apps')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


if __name__ == '__main__':
    with SensitiveData() as data:
        id1 = data.get('app_id_l1')
        token1 = data.get('app_key_l1')
        id2 = data.get('app_id_l2')
        token2 = data.get('app_key_l2')

    print(id1, token1, id2, token2)
