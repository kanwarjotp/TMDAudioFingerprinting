import wave

import pyaudio


class Recorder:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5

    def __init__(self):
        self._p = pyaudio.PyAudio()  # instantiating PyAudio

    def __del__(self):
        self._p.terminate()

    def record_audio(self):
        with wave.open('wavs/recorded_wavs/output.wav', 'wb') as wf:
            wf.setnchannels(Recorder.CHANNELS)
            wf.setsampwidth(self._p.get_sample_size(Recorder.FORMAT))
            wf.setframerate(Recorder.RATE)

            stream = self._p.open(
                format=Recorder.FORMAT,
                channels=Recorder.CHANNELS,
                rate=Recorder.RATE, input=True,
                input_device_index=1,
                frames_per_buffer=Recorder.CHUNK
            )

            print('Recording...')
            for _ in range(0, Recorder.RATE // Recorder.CHUNK * Recorder.RECORD_SECONDS):
                print(stream.read(Recorder.CHUNK))
                wf.writeframes(stream.read(Recorder.CHUNK))
            print('Done')

            stream.close()

    def device_info(self):
        print(self._p.get_default_host_api_info())
        print(self._p.get_device_info_by_index(1))


def play():
    p = pyaudio.PyAudio()

    with wave.open('wavs/recorded_wavs/output.wav', 'rb') as wf:

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(8192)
        print(data)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(8192)

        stream.stop_stream()
        stream.close()
        p.terminate()


test_rec = Recorder()
# test_rec.device_info()
test_rec.record_audio()

