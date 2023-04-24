import mysql.connector
from mysql.connector import errorcode
import config


class SQLConnection:
    TABLES = {
        'fingerprint': '''
            CREATE TABLE fingerprint ( 
                 hash binary(10) not null,
                 song_id mediumint unsigned not null, 
                 offset int unsigned not null, 
                 INDEX(hash),
                 UNIQUE(song_id, offset, hash)
            )
            ''',
        'song': '''
            CREATE TABLE song (
            song_id mediumint unsigned not null auto_increment, 
            song_name varchar(250) not null,
            fingerprinted tinyint default 0,
            PRIMARY KEY (song_id),
            UNIQUE KEY song_id (song_id)
        )
        '''
    }

    def __init__(self):
        try:
            self._cnx = mysql.connector.connect(**config.cnxn_conf)
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

    def __del__(self):
        self._cnx.close()

    def create_database(self, db_name: str):
        # create the database if it doesn't exist
        self._cur.execute('''CREATE DATABASE IF NOT EXISTS {0}'''.format(db_name))
        self._cnx.commit()
        print("Database Created: ", db_name)

    def use_database(self, db_name: str):
        try:
            self._cur.execute("USE {}".format(db_name))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(db_name))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(db_name)
                print("Database {} created successfully.".format(db_name))
                self._cnx.database = db_name
            else:
                print(err)
                exit(1)

    def create_tables(self):
        for table_name in SQLConnection.TABLES:
            try:
                self._cur.execute(SQLConnection.TABLES[table_name])
                self._cnx.commit()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Already Exists")
                else:
                    print(err.msg)

    def insert_fingerprint(self, fingerprint: tuple):
        # (hash_val, (song_id, freq))
        try:
            add_fingerprint = ("INSERT INTO fingerprint "
                               "(hash, song_id, offset) "
                               "VALUES (%s, %s, %s)")

            data_fingerprint = (fingerprint[0], fingerprint[1][0], fingerprint[1][1])

            self._cur.execute(add_fingerprint, data_fingerprint)
            self._cnx.commit()
        except mysql.connector.Error as err:
            print(err.msg)

    def insert_song(self, song_name: str):
        add_song = '''INSERT INTO song (song_name) VALUE ("{}")'''

        self._cur.execute(add_song.format(song_name))
        self._cnx.commit()
