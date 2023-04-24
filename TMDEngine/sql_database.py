import mysql.connector
from mysql.connector import errorcode
import config


class SQLConnection:
    def __init__(self):
        try:
            self._cnx = mysql.connector.connect(**config.database_conf)
            self._cur = self._cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close_cnx(self):
        self._cnx.close()

    def create_database(self, db_name: str):
        # create the database if it doesn't exist
        self._cur.execute('''CREATE DATABASE IF NOT EXISTS {0}'''.format(db_name))
        self._cnx.commit()
        print("Database Created: ", db_name)


test_cnx = SQLConnection()
test_cnx.create_database("TMD_SCHEMA")
