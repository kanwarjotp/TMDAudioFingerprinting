import sqlite3

DATABASE_NAME = 'FINGERPRINTS_SCHEMA'

''' create fingerprint table
CREATE TABLE fingerprint(
                    hash BINARY(10) NOT NULL,
                    song_id MEDIUMINT UNSIGNED NOT NULL,
                    offset INT UNSIGNED NOT NULL,
                    UNIQUE(hash, song_id, offset)
                    );'''

'''CREATE UNIQUE INDEX hash on fingerprint(hash);'''

'''CREATE TABLE song(
                song_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                song_name VARCHAR(250) UNIQUE NOT NULL,
                fingerprinted TINYINT DEFAULT 0
                );'''


def insert_fingerprints(fingerprint_list, verbose=False):
    """

    :param fingerprint_list: the fingerprints of a song,  to be added to the database
    :param verbose: Boolean, set True to display the number of hashes found already present in the table.
    :return: None
    """
    num_duplicates = 0
    # establishing a connection to the database
    db_conn = sqlite3.connect(DATABASE_NAME)
    db_cursor = db_conn.cursor()
    record_no = 0
    for fingerprint in fingerprint_list:
        hash_value = fingerprint[0]
        song_id = fingerprint[1][0]
        time_offset = fingerprint[1][1]

        sqlite_cmd = '''INSERT INTO fingerprint (hash, song_id, offset) VALUES("{0}", "{1}", "{2}");''' \
            .format(hash_value, song_id, time_offset)

        try:
            db_cursor.execute(sqlite_cmd)
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed:" in e.__str__():  # the unique constraint is violated
                # trying to add duplicate values
                num_duplicates += 1
                continue
            else:
                db_conn.rollback()  # rolling back the database to the last commit
                raise e

        record_no += 1
        db_conn.commit()
        if verbose:
            print("record num: ", record_no)
    db_conn.close()

    if verbose:
        print("Number of Duplicates :", num_duplicates)


def insert_song(song_name):
    """

    :param song_name: the name of the song, to be added to the database
    :return: song_id and fingerprinted_val: returns the song_id and fingerprinted value from the database, after updating the database

    """
    db_conn = sqlite3.connect(DATABASE_NAME)
    db_cursor = db_conn.cursor()

    # sets the default fingerprinted value and assigns the song id
    try:
        sqlite_cmd = '''INSERT INTO song (song_name) VALUES ("{0}");'''.format(song_name)
        db_cursor.execute(sqlite_cmd)
        db_conn.commit()
    except sqlite3.DatabaseError as e:
        if "UNIQUE constraint failed:" in e.__str__():
            print("Song already in Database\n(SongID\tFingerprinted{0:N/1:Y})")
        else:
            print(sqlite_cmd)
            raise e

    # extracting the song_id
    db_conn.row_factory = sqlite3.Row
    sqlite_cmd = '''SELECT song_id, fingerprinted FROM song WHERE song_name == "{0}"'''.format(song_name)
    db_cursor.execute(sqlite_cmd)

    rows = db_cursor.fetchall()

    s_id = None
    f_val = None
    for entry in rows:
        s_id = entry[0]
        f_val = entry[1]

    return s_id, f_val


def display_fingerprint_table(hash_lookup):
    db_conn = sqlite3.connect(DATABASE_NAME)
    db_conn.row_factory = sqlite3.Row

    db_cursor = db_conn.cursor()
    sqlite_cmd = '''SELECT * FROM fingerprint where hash="{0}";'''.format(hash_lookup)
    db_cursor.execute(sqlite_cmd)

    rows = db_cursor.fetchall()
    db_conn.close()

    for entry in rows:
        print(entry['hash'], entry['song_id'], entry['offset'])


print(insert_song("katy_perry"))

