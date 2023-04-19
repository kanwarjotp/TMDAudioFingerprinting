import fingerprint
import sqlite3


class Recognizer:
    def __init__(self, audio_file):
        """

        :param:
        audio_file: String, address of audio file to recognize
        """
        # TODO: change this to be the wav file directly
        self._audio_file = audio_file

    def recognize_song(self):
        fingerprinted = fingerprint.Fingerprinter(self._audio_file)

        hashes_of_sample = fingerprinted.get_fingerprint()

        matched_fingerprints_from_db = self._find_matches(hashes_of_sample)

        song_id = self._align_matches(matched_fingerprints_from_db)

        return song_id


    def _find_matches(self, hashes_of_song):

        pass

    def _align_matches(self, matched_fingerprints):
        pass
