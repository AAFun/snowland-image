import configparser
import pymysql


cp = configparser.ConfigParser()


class MysqlConnection:

    def __init__(self, session, file_name='db.conf'):
        cp.read(file_name)
        self.database = cp.get(session, 'database')
        self.user = cp.get(session, 'user')
        self.password = cp.get(session, 'password')
        self.host = cp.get(session, 'host')
        self.port = int(cp.get(session, 'port'))
        self.connection = None

    def __enter__(self):
        self.connection = pymysql.connect(**{'database': self.database,
                                             'user': self.user,
                                             'password': self.password,
                                             'port': self.port,
                                             'host': self.host})

        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None:
            self.connection.close()


class Cursor:
    def __init__(self, connection):
        self.connection = connection
        self._cursor = None

    def __enter__(self):
        self._cursor = self.connection.cursor()
        return self._cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._cursor is not None:
            self._cursor.close()
