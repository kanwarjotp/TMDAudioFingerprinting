# final run script for using the recognition application
import fingerprint
import recognize
import dev.config as conf

user_sample = conf.test_rec   # path to user's recording

fprinter_for_sample = fingerprint.Fingerprint(user_sample)
fprints_of_sample = fprinter_for_sample.get_fingerprint(verbose=True)  # the fingerprints for sample
print("Fingerprints Created")  # TODO: very few fingerprints are actually matched, have to make this more meaningful

testing_ = fprints_of_sample
# lookup the fingerprints using hash matching
matching_fingerprints_in_db = recognize.look_for_matches(testing_)  # trying at first on a2 fingerprints
print("Matching Fingerprints Found")
not_matched_at_all = 0
for i in matching_fingerprints_in_db.keys():
    print(i, matching_fingerprints_in_db[i])
    if not matching_fingerprints_in_db[i]:
        not_matched_at_all += 1

print("Useless sample fingerprints: ", round((not_matched_at_all / len(testing_)) * 100, 2), "%")
# this is useless because at least the one from the original song should have matched, that at least one entry in the
# list no matches clearly signify that we need to up the quality of our fingerprints:
# up the thresholds, min intensity
all_pairs = []
for f in matching_fingerprints_in_db.keys():
    if matching_fingerprints_in_db[f]:
        all_pairs += matching_fingerprints_in_db[f]

print("\n\n all pairs : \n {} \n\n".format(all_pairs))

song_id, dict_songs = recognize.find_final_song_id(all_pairs)

print("\n\n*************\n{0}\n*************\n\n, {1}".format(song_id, dict_songs))
exit(0)
# align the fingerprints received from the database and store them as (song_id, time_difference)
aligned_matching_fingerprints = []
for fingerprint_of_sample in matching_fingerprints_in_db.keys():
    aligned_matching_fingerprints.append(
        recognize.align_matches(
            fingerprint_of_sample, matching_fingerprints_in_db[fingerprint_of_sample]
        )
    )
print("Fingerprints aligned")

# once the matches have been aligned, just find the highest count for a difference, that one is the song_id
count_for_each_diff = {}
print(aligned_matching_fingerprints)
