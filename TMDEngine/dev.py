# from database import insert_song, change_song_name
# import sqlite3
#
# files_to_fingerprint = [
#     "All_Eyez_On_Me-Tupac",
#     "Caviar-Diljit Dosanjh prod. Intense",
#     "Despacito_Luis-Fonsi ft. Dady_Yankee",
#     "Levels-Sidhu Moosewala",
#     "Perfect-Ed Sheeran",
#     "The_Monster-Eminem ft. Rihanna",
#     "Kendrick Lamar-Bitch, Don't Kill My Vibe (Explicit)"
# ]
# # s_ids = []
# # for files in files_to_fingerprint:
# #     s_ids.append([files, insert_song(files)])
#
# # for i in s:
# #     db_conn = sqlite3.connect("FINGERPRINTS_SCHEMA")
# #     db_cursor = db_conn.cursor()
# #
# #     sqlite_cmd = '''UPDATE fingerprint SET song_id = {1} WHERE song_id = "{0}" '''.format(i[0], i[1][0])
# #     print(sqlite_cmd)
# #
# #     db_cursor.execute(sqlite_cmd)
# #     db_conn.commit()
# #     db_conn.close()
#
#
# old_names = ["All_Eyez_On_Me_Tupac",
# "Caviar_Diljit_Dosanjh_Intense",
# "Despacito_Luis_Fonsi_Dady_Yankee",
# "Levels_Sidhu_Moosewala",
# "Perfect_Ed Sheeran",
# "The_Monster_Eminem_Rihanna",
# "Kendrick Lamar - Bitch, Don't Kill My Vibe (Explicit)",
# "Waffle_House_Jonas_Brothers"
# ]
#
# new_names = []
# for i in old_names:
#     new_names += [(i, i.replace("_", " "))]
#
# print(new_names)
#
# names_list = [('All_Eyez_On_Me_Tupac', 'All Eyez On Me-Tupac'),
#               ('Caviar_Diljit_Dosanjh_Intense', 'Caviar-Diljit Dosanjh Intense'),
#               ('Despacito_Luis_Fonsi_Dady_Yankee', 'Despacito-Luis Fonsi Dady Yankee'),
#               ('Levels_Sidhu_Moosewala', 'Levels-Sidhu Moosewala'),
#               ('Perfect_Ed Sheeran', 'Perfect-Ed Sheeran'),
#               ('The_Monster_Eminem_Rihanna', 'The Monster-Eminem Rihanna'),
#               ("Kendrick Lamar - Bitch, Don't Kill My Vibe (Explicit)", "Kendrick Lamar-Bitch, Don't Kill My Vibe (Explicit)"),
#               ('Waffle_House_Jonas_Brothers', 'Waffle House-Jonas Brothers')]
#
# for names in names_list:
#     change_song_name(names[0], names[1])
