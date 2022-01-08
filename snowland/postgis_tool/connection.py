import configparser
import psycopg2


cp = configparser.ConfigParser()


class PGConnection:

    def __init__(self, session, file_name='db.conf'):
        cp.read(file_name)
        self.database = cp.get(session, 'database')
        self.user = cp.get(session, 'user')
        self.password = cp.get(session, 'password')
        self.host = cp.get(session, 'host')
        self.port = int(cp.get(session, 'port'))
        self.connection = None

    def __enter__(self):
        self.connection = psycopg2.connect(
            "dbname='%(dbname)s' user='%(user)s' password='%(password)s' port='%(port)s' host='%(host)s'" % {
                'dbname': self.database, 'user': self.user, 'password': self.password, 'port': self.port, 'host': self.host})

        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None:
            self.connection.close()
