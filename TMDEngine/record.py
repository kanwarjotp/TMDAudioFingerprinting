import sys
import wave

import pyaudio

print(pyaudio.get_portaudio_version())


class Recorder:
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1 if sys.platform == 'darwin' else 2
    RATE = 44100
    RECORD_SECONDS = 5

    def __init__(self):
        self._p = pyaudio.PyAudio()  # instantiating PyAudio
        self._recorded_audio = None

    def __del__(self):
        self._p.terminate()

    def record_audio(self):
        with wave.open('wavs/recorded_wavs/output.wav', 'wb') as wf:
            wf.setnchannels(Recorder.CHANNELS)
            wf.setsampwidth(self._p.get_sample_size(Recorder.FORMAT))
            wf.setframerate(Recorder.RATE)

            stream = self._p.open(format=Recorder.FORMAT, channels=Recorder.CHANNELS, rate=Recorder.RATE, input=True)

            print('Recording...')
            for _ in range(0, Recorder.RATE // Recorder.CHUNK * Recorder.RECORD_SECONDS):
                print(stream.read(Recorder.CHUNK))
                wf.writeframes(stream.read(Recorder.CHUNK))
            print('Done')

            stream.close()

    def device_info(self):
        print(self._p.get_default_host_api_info())


test_rec = Recorder()
test_rec.device_info()
test_rec.record_audio()
