from scipy.io import wavfile


class Fingerprint:
    def __init__(self, song):
        """
        Params:
        song, a string for the address of the file
        exposes a get_fingerprint method which returns a hash value, representing the fingerprint
        """
        self._song = song
        self._wav_info = None
        self._spectrum = None
        self._figure = None
        self._coordinates = None
        self._hash = None

    def get_fingerprint(self):
        self._convert_to_wav()
        return self._hash

    def _convert_to_wav(self):
        sample_rate, song_data = wavfile.read(self._song)

        data_dict = {
            'sample_rate': sample_rate,
            'song_data': song_data
        }

        self._wav_info = data_dict



fingerprint_1 = Fingerprint("F:\AF\wavs\Jonas Brothers.wav")
# testing class structure
# fingerprint = fingerprint_1.get_fingerprint()
# print(fingerprint_1._wav_info)
