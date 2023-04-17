import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile
from matplotlib.mlab import specgram

NFFT_VALUE = 4096
OVERLAP_VALUE = 2048

class Fingerprint:
    def __init__(self, song, title):
        """
        Params:
        song, a string for the address of the file
        exposes a get_fingerprint method which returns a hash value, representing the fingerprint
        """
        self._title = title
        self._song = song
        self._wav_info = None
        self._spectrum = None
        self._figure = None
        self._coordinates = None
        self._hash = None

    def get_fingerprint(self, plot=False):
        self._convert_to_wav()
        print("wav file generated")
        self._generate_spectrum()
        print("spectrum generated")

        if plot:  # plot if requested
            temp_fig = self._figure
            plt.show()

        return self._hash

    def _convert_to_wav(self):
        sample_rate, song_data = wavfile.read(self._song)

        data_dict = {
            'sample_rate': sample_rate,
            'song_data': song_data
        }

        self._wav_info = data_dict

    def _generate_spectrum(self):
        song_left_channel = self._wav_info['song_data'][:, 0]

        spectrum, freqs, times = specgram(
            x=song_left_channel,
            Fs=self._wav_info['sample_rate'],
            NFFT=NFFT_VALUE,
            noverlap=OVERLAP_VALUE
        )

        spectrum[spectrum == 0] = 1e-6  # changing 0 values to 1e-6

        fig = plt.figure(figsize=(20, 8), facecolor='white')
        Z = 10.0 * np.log10(spectrum)  # apply log transform since specgram() returns linear array
        Z = np.flipud(Z)
        extent = 0, np.amax(times), freqs[0], freqs[-1]
        plt.imshow(Z, cmap='viridis', extent=extent)
        plt.xlabel('Time bin')
        plt.ylabel('Frequency [Hz]')
        plt.title(self._title)
        plt.axis('auto')
        ax = plt.gca()
        ax.set_xlim([extent[0], extent[1]])
        ax.set_ylim([extent[2], extent[3]])

        self._figure = fig



fingerprint_1 = Fingerprint("F:\AF\wavs\Jonas Brothers.wav", "JB")
# testing class structure
# fingerprint = fingerprint_1.get_fingerprint(plot=True)
# print(fingerprint_1._wav_info)
