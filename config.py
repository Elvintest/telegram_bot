import mysql.connector
import mysql.connector.pooling
import os, sys
from dotenv import load_dotenv

home = os.getcwd()
dotenv_path = os.path.join(home, 'variables.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print('variables wasnt found')


class MainConfig:
    dbconfig = {'host': os.environ['HOST'],
                'user': os.environ['USER'],
                'password': os.environ['PASSWORD_DB'],
                'database': os.environ['DATA_BASE_NAME'],
                'charset': 'utf8',
                'pool_size': 10,
                'pool_name': 'Pool_connections',
                'pool_reset_session': False}

    bot_key = os.environ['BOT_KEY']


class DB:

    def __init__(self):
        self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(**MainConfig.dbconfig)

    def connect(self):
        try:
            self.conn = self.cnxpool.get_connection()
        except Exception:
            print("problems with getting connection from Pool_connections")

    def query(self, sql, *args):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, *args)
            return self.cursor.fetchall()
        except Exception as error:
            print(f' While readind data from database there were db errors {error}')

    def execute(self, sql, variables):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, variables)
            self.conn.commit()
        except Exception as error:
            print(f' While execution there were db errors {error}')

    def close(self):
        self.conn.close()
