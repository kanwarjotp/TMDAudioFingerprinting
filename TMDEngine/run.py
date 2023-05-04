# final run script for using the recognition application
import fingerprint
import recognize
import dev.config as conf
import sql_database as db

user_sample = conf.test_rec   # path to user's recording

fprinter_for_sample = fingerprint.Fingerprint(user_sample)
fprints_of_sample = fprinter_for_sample.get_fingerprint(verbose=True)  # the fingerprints for sample
print("Fingerprints Created")  # TODO: very few fingerprints are actually matched, have to make this more meaningful

testing_ = fprints_of_sample
# lookup the fingerprints using hash matching
matching_fingerprints_in_db = recognize.look_for_matches(testing_)  # trying at first on a2 fingerprints
print("Matching Fingerprints Found:")
not_matched_at_all = 0
for i in matching_fingerprints_in_db.keys():
    print(i, matching_fingerprints_in_db[i])
    if not matching_fingerprints_in_db[i]:
        not_matched_at_all += 1

print("Unused Recording Fingerprints: ", round((not_matched_at_all / len(testing_)) * 100, 2), "%")
# this is useless because at least the one from the original song should have matched, that at least one entry in the
# list no matches clearly signify that we need to up the quality of our fingerprints:
# up the thresholds, min intensity
all_pairs = []
for f in matching_fingerprints_in_db.keys():
    if matching_fingerprints_in_db[f]:  # the match list is not empty
        all_pairs += matching_fingerprints_in_db[f]

print("\n\n Num of Pairs(Matches) : \n {} \n\n".format(len(all_pairs)))

song_id, dict_songs = recognize.find_final_song_id(all_pairs)

print("\n\n***\n{0}\n***\n\nDict of all matches per Song{1}".format(song_id, dict_songs))
print("Correct Matches: {} %".format(round(dict_songs[song_id] / len(all_pairs), 2)))

db_songs = db.SQLConnection()
print("Song Prediction: ", db_songs.find_song(song_id))

