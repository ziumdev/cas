import psycopg2
from psycopg2.extras import RealDictCursor
import extConfig


class Database:

    def __init__(self, host=extConfig.dbHost, port=extConfig.dbPort, dbName=extConfig.dbName, user=extConfig.dbUser, password=extConfig.dbPassword):
        self.conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbName)
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def parameterQuery(self, query, param):
        self.cursor.execute(query,param)
        rows = self.cursor.fetchall()
        return rows

    def insertQuery(self, query, param):
        self.cursor.execute(query, param)
        self.conn.commit()

    def query(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchone()
        return rows

    def close(self):
        self.cursor.close()
        self.conn.close()