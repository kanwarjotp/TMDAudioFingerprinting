import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile
from matplotlib.mlab import specgram
from skimage.feature import peak_local_max

class Fingerprint:

    NFFT_VALUE = 4096
    OVERLAP_VALUE = 2048
    MIN_DISTANCE_PEAKS = 20
    THRESHOLD_ABS_PEAKS = 20

    def __init__(self, song, title):
        """

        :param song: a string for the address of the file
        :return Fingerprint Object: exposes a get_fingerprint method which returns a hash value, representing the fingerprint
        """
        self._title = title
        self._song = song
        self._wav_info = None
        self._spectrum = None
        self._coordinates = None
        self._hash = None

    def get_fingerprint(self, plot=False):
        """

        :param plot: set True if th plots are desired, False otherwise
        :return: hash value representing the fingerprint
        """
        self._convert_to_wav()
        print("wav file generated")
        self._generate_spectrum(plot=plot)
        print("spectrum generated")
        self._find_peaks()
        print("peaks generated")

        if plot:  # plot if requested
            fig = plt.figure(figsize=(20, 8), facecolor='white')
            plt.imshow(self._spectrum['spectrum'], cmap='viridis')
            plt.scatter(self._coordinates[:, 1], self._coordinates[:, 0])
            ax = plt.gca()
            plt.xlabel('Time bin[s]')
            plt.ylabel('Frequency[Hz]')
            plt.title(self._title, fontsize=18)
            plt.axis('auto')
            ax.set_xlim([0, len(self._spectrum['times'])])
            ax.set_ylim([len(self._spectrum['freqs']), 0])
            ax.xaxis.set_ticklabels([])
            ax.yaxis.set_ticklabels([])
            plt.show()

        return self._hash

    def _convert_to_wav(self):
        sample_rate, song_data = wavfile.read(self._song)

        data_dict = {
            'sample_rate': sample_rate,
            'song_data': song_data
        }

        self._wav_info = data_dict

    def _generate_spectrum(self, plot):
        song_left_channel = self._wav_info['song_data'][:, 0]

        spectrum, freqs, times = specgram(
            x=song_left_channel,
            Fs=self._wav_info['sample_rate'],
            NFFT=Fingerprint.NFFT_VALUE,
            noverlap=Fingerprint.OVERLAP_VALUE
        )

        spectrum[spectrum == 0] = 1e-6  # changing 0 values to 1e-6
        Z = 10.0 * np.log10(spectrum)  # apply log transform since specgram() returns linear array
        Z = np.flipud(Z)

        if plot:
            plt.figure(figsize=(20, 8), facecolor='white')
            extent = 0, np.amax(times), freqs[0], freqs[-1]
            Z = np.flipud(Z)
            plt.imshow(Z, cmap='viridis', extent=extent)
            plt.xlabel('Time bin')
            plt.ylabel('Frequency [Hz]')
            plt.title(self._title + ", close to continue")
            plt.axis('auto')
            ax = plt.gca()
            ax.set_xlim([extent[0], extent[1]])
            ax.set_ylim([extent[2], extent[3]])
            plt.show()

        self._spectrum = Z

    def _find_peaks(self):
        self._coordinates = peak_local_max(
            self._spectrum,
            min_distance=Fingerprint.MIN_DISTANCE_PEAKS,
            threshold_abs=Fingerprint.THRESHOLD_ABS_PEAKS
        )

    def _generate_hash(self):
        pass


fingerprint_1 = Fingerprint("F:\AF\wavs\Jonas Brothers.wav", "JB")
# testing class structure
fingerprint = fingerprint_1.get_fingerprint(plot=True)
# print(fingerprint_1._wav_info)
