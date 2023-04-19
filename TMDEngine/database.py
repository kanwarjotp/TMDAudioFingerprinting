import sqlite3

DATABASE_NAME = 'FINGERPRINTS_SCHEMA'

'''CREATE TABLE fingerprint(
                    hash BINARY(10) NOT NULL,
                    song_id MEDIUMINT UNSIGNED NOT NULL,
                    offset INT UNSIGNED NOT NULL,
                    UNIQUE(hash, song_id, offset)
                    );'''

'''CREATE UNIQUE INDEX hash on fingerprint(hash);'''


def insert_fingerprints(fingerprint_list, verbose=False):
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

display_fingerprint_table("e7bcab739ebd2b1cb2d3")