from pymongo import MongoClient
from config import settings
class ConnMongo(object):
    username = settings.MONGO_USER
    password = settings.MONGO_PASSWORD
    host = settings.MONGO_HOST
    port = settings.MONGO_PORT

    def __new__(self):
        if not hasattr(self, 'instance'):
            uri = f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}' \
                if self.username and self.password else f'mongodb://{self.host}:{self.port}'
            self.instance = super(ConnMongo, self).__new__(self)
            self.instance.conn = MongoClient(uri)
        return self.instance


def conn_db(collection):
    db_name = settings.MONGO_DATABASE
    conn = ConnMongo().conn
    if db_name:
        return conn[db_name][collection]

if __name__ == '__main__':
    # 测试代码
    conn_db("subdomain")
