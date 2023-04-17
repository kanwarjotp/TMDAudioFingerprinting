class Fingerprint:
    def __init__(self, song):
        self.__song = song
        self.__wav_file = None
        self.__spectrum = None
        self.__figure = None
        self.__coordinates = None
        self.__hash = None

    def get_fingerprint(self):
        return self.__hash

