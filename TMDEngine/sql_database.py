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
            song_name varchar(250) unique not null,
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

    # not required if conf,py specifies the database to be used.
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
            add_fingerprint = "INSERT INTO fingerprint (hash, song_id, offset) VALUES (UNHEX('{0}'), {1}, {2})"
            self._cur.execute(add_fingerprint.format(fingerprint[0], fingerprint[1][0], fingerprint[1][1]))
            self._cnx.commit()
        except mysql.connector.Error as err:
            print(err.msg)

    def insert_song(self, song_name: str):
        s_id = []

        try:
            add_song = '''INSERT INTO song (song_name) VALUE ("{}")'''

            self._cur.execute(add_song.format(song_name))
            self._cnx.commit()
        except mysql.connector.Error as err:
            print(err.msg)

        cursor = self._cnx.cursor()
        select_song_id = '''SELECT song_id FROM song WHERE song_name = "{}"'''
        cursor.execute(select_song_id.format(song_name))

        for result in cursor.fetchall():
            s_id.append(result[0])
        cursor.close()
        return s_id[0]

    def find_fingerprint(self, fprint_hash: str):
        fingerprints = []
        cursor = self._cnx.cursor()

        # finding out how the hash is stored in sql and then recreating it here to query
        find_hex_not_sql = '''select hex((unhex('{}')))'''.format(fprint_hash)
        cursor.execute(find_hex_not_sql)
        sub_20 = 0
        for i in cursor:
            sub_20 = i[0]
        zeroes_to_add = 20 - len(sub_20)
        final_hash_query = sub_20 + ("0" * zeroes_to_add)  # hash to query with

        # querying the hash
        select_fprint = '''select hex(hash), song_id, offset from fingerprint where
                            hex(hash) = "{}"'''
        cursor.execute(select_fprint.format(final_hash_query))
        for result in cursor:
            fingerprints.append(result)
        cursor.close()

        return fingerprints

    def find_song(self, song_id: int):
        song_info = []
        select_song = '''SELECT song_id, song_name, fingerprinted FROM song WHERE song_id = {}'''

        try:
            cursor = self._cnx.cursor()
            cursor.execute(select_song.format(song_id))
        except mysql.connector.Error as err:
            print(err)

        for result in cursor:
            song_info.append(result)

        cursor.close()
        return song_info


test_cnx = SQLConnection()
