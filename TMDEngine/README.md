
## Development Notes:

1. flexible typing iun SQLITE allows us to store values as integere without worrying about upper limits hence the
<b>song</b> table can use INTEGER without being concerned about the number of songs
2. 

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

1. the hash was stored in a binary BLOB in mysql, whihc was not <b>comparable</b>, so i had to unhex it while saving, this was to save space and then re-hex it while querying(cast as method were not working).
Finally, since the hex was stored as a binary string of 20 characters i had to do the same to the query submitted by the find_fingerprint() function in order to make the query work. the code for the same can be found in 
commit: <u>b73f44ed Kanwar Jot Parkash Singh <52690070+kanwarjotp@users.noreply.github.com> on 25-Apr-23 at 05:38</u>