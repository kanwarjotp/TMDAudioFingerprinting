import hashlib
import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile
from matplotlib.mlab import specgram
from skimage.feature import peak_local_max


class Fingerprint:
    NFFT_VALUE = 4096
    OVERLAP_VALUE = 2048
    MIN_DISTANCE_PEAKS = 15
    MIN_INTENSITY_OF_PEAKS = 20 # the more this value, less the noise errors
    TIME_INTERVAL_PRECISION = 3  # 0 = second, 3 = millisecond
    MAX_SEGMENT_TO_FINGERPRINT = 15
    MIN_TIME_DIFF = 0  # min time diff between peak frequencies

    def __init__(self, song, song_id):
        """

        :param song: a string for the address of the file
        :return Fingerprint Object: exposes a get_fingerprint method which returns a hash value,
         representing the fingerprint
        """
        self._song_id = song_id
        self._song = song
        self._wav_info = {
            'sample_rate': None,
            'song_data': None
        }
        self._spectrum = {
            'spectrum': None,
            'times': None,
            'freqs': None
        }
        self._coordinates = None
        self._peaks = None
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
            plt.figure(figsize=(20, 8), facecolor='white')
            plt.imshow(self._spectrum['spectrum'], cmap='viridis')
            plt.scatter(self._coordinates[:, 1], self._coordinates[:, 0])
            ax = plt.gca()
            plt.xlabel('Spectrogram Width Units')
            plt.ylabel('Spectrogram Height Units')
            plt.title(self._song_id, fontsize=18)
            plt.axis('auto')
            ax.set_xlim([0, len(self._spectrum['times'])])
            ax.set_ylim([len(self._spectrum['freqs']), 0])
            ax.xaxis.set_ticklabels([])
            ax.yaxis.set_ticklabels([])
            plt.show()

        self._generate_hash()
        print("hash generated")
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
        Z = np.flipud(Z)  # inverting y-axis of spectrum

        if plot:
            plt.figure(figsize=(20, 8), facecolor='white')
            extent = 0, np.amax(times), freqs[0], freqs[-1]
            Z = 10.0 * np.log10(spectrum)  # apply log transform since specgram() returns linear array
            Z = np.flipud(Z)
            plt.imshow(Z, cmap='viridis', extent=extent)
            plt.xlabel('Time bin')
            plt.ylabel('Frequency [Hz]')
            plt.axis('auto')
            ax = plt.gca()
            ax.set_xlim([0, extent[1]])
            ax.set_ylim([freqs[0], freqs[-1]])
            plt.show()

        self._spectrum = {
            'spectrum': Z,
            'times': times,
            'freqs': freqs
        }

    def _find_peaks(self):
        # finding peaks using scipy
        self._coordinates = peak_local_max(
            self._spectrum['spectrum'],
            min_distance=Fingerprint.MIN_DISTANCE_PEAKS,
            threshold_abs=Fingerprint.MIN_INTENSITY_OF_PEAKS
        )

        peaks = []  # list to store peaks for the songs

        ht_of_spec = self._spectrum['spectrum'].shape[0]
        wdt_of_spec = self._spectrum['spectrum'].shape[1]

        length_of_song = round(np.amax(self._spectrum['times']), Fingerprint.TIME_INTERVAL_PRECISION)
        max_freq_of_song = self._spectrum['freqs'][-1]

        single_unit_time = round((length_of_song / wdt_of_spec), Fingerprint.TIME_INTERVAL_PRECISION)
        single_unit_freq = round((max_freq_of_song / ht_of_spec))

        for i in self._coordinates:
            # converting x coordinates to time in seconds
            time_coordinate = round(single_unit_time * i[1], Fingerprint.TIME_INTERVAL_PRECISION)

            # converting y coordinates to frequency in Hz
            freq_coordinates = round(single_unit_freq * (ht_of_spec - i[0]))

            # storing the pair in peaks
            peaks.append((time_coordinate, freq_coordinates))
            pass

        self._peaks = peaks

    def _generate_hash(self):

        hashed = set()  # preventing redundant hashes

        hashes = []
        peaks = self._peaks

        for i in range(len(peaks)):
            for j in range(Fingerprint.MAX_SEGMENT_TO_FINGERPRINT):
                if i+j < len(peaks) and not (i, i+j) in hashed:
                    f1 = peaks[i][1]
                    f2 = peaks[i + j][1]
                    t1 = peaks[i][0]
                    t2 = peaks[i + j][0]
                    t_diff = t2 - t1

                    if t_diff >= Fingerprint.MIN_TIME_DIFF:
                        # hash this value
                        h = hashlib.sha1(("{0}{1}{2}".format(str(f1), str(f2), str(t_diff))).encode('utf-8'))
                        # truncating the hash to conserve storage
                        hashes.append((h.hexdigest()[0:20], (self._song_id, t1)))

                    hashed.add((i, i+j))

        self._hash = hashes