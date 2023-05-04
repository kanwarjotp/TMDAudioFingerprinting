
## Development Notes:

1. for unknown songs, the song_id will be set to 0 to be passed to Fingerprint Object.
2.  The way matched_fingerprints are stored in recognize.py is quite confusing and increases the space complexity, 
but it prevents the  function from going into a Quadratic time complexity, as the other way would have me aligning 
the fingerprints as they are found and directly storing the (song_id, difference pairs)
which is the better option in terms of logical clarity, but costly.
3. <b>Song Prediction now works.</b>

## Database
### Song Table
1. stores song_id
   1. uniquely identifies a song
   2. stores info used to access the fingerprints in the fingerprint table

2. stores song_name
   1. is unique to prevent wastage of space in songs table
   2. can be kept not unique, as fingerprint's table keep track of duplicate hashes itself

3. stores fingerprinted
    1. stores a flag, helps decide which song to fingerprint.

## Challenges Solved

1. the hash was stored in a binary BLOB in mysql, which was not <b>comparable</b>, so i had to unhex it while saving, this was to save space and then re-hex it while querying(cast as method were not working).
Finally, since the hex was stored as a binary string of 20 characters I had to do the same to the query submitted by the find_fingerprint() function in order to make the query work. the code for the same can be found in 
commit: <u>b73f44ed Kanwar Jot Parkash Singh <52690070+kanwarjotp@users.noreply.github.com> on 25-Apr-23 at 05:38</u>
