from database import insert_song
import sqlite3

files_to_fingerprint = [
    "All_Eyez_On_Me_Tupac",
    "Caviar_Diljit_Dosanjh_Intense",
    "Despacito_Luis_Fonsi_Dady_Yankee",
    "Levels_Sidhu_Moosewala",
    "Perfect_Ed Sheeran",
    "The_Monster_Eminem_Rihanna",
    "Kendrick Lamar - Bitch, Don't Kill My Vibe (Explicit)"

]
# s_ids = []
# for files in files_to_fingerprint:
#     s_ids.append([files, insert_song(files)])


s = [['All_Eyez_On_Me_Tupac', (1, 0)],
     ['Caviar_Diljit_Dosanjh_Intense', (2, 0)],
     ['Despacito_Luis_Fonsi_Dady_Yankee', (3, 0)],
     ['Levels_Sidhu_Moosewala', (4, 0)],
     ['Perfect_Ed Sheeran', (5, 0)],
     ['The_Monster_Eminem_Rihanna', (6, 0)],
     ["Kendrick Lamar - Bitch, Don't Kill My Vibe (Explicit)", (7, 0)]]

for i in s:
    db_conn = sqlite3.connect("FINGERPRINTS_SCHEMA")
    db_cursor = db_conn.cursor()

    sqlite_cmd = '''UPDATE fingerprint SET song_id = {1} WHERE song_id = "{0}" '''.format(i[0], i[1][0])
    print(sqlite_cmd)

    db_conn
