# final run script for using the recognition application
import fingerprint
import recognize
import dev.config as conf

user_sample = conf.test_rec   # path to user's recording

fprinter_for_sample = fingerprint.Fingerprint(user_sample)
fprints_of_sample = fprinter_for_sample.get_fingerprint(verbose=True)  # the fingerprints for sample
print("Fingerprints Created")

# lookup the fingerprints using hash matching
matching_fingerprints_in_db = recognize.look_for_matches(fprints_of_sample[:2])  # trying at first on a2 fingerprints
print("Matching Fingerprints Found")


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
count_of_vals_for_diff = {}
print(aligned_matching_fingerprints)
