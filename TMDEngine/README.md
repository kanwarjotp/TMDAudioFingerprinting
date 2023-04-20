
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