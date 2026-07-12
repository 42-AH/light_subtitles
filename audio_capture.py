import threading

import numpy as np
import soundcard as sc


class AudioCapture(threading.Thread):
    def __init__(self, transcriber, on_text, samplerate=16000, blocksize=4000):
        super().__init__(daemon=True)
        self.transcriber = transcriber
        self.on_text = on_text
        self.samplerate = samplerate
        self.blocksize = blocksize
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def run(self):
        speaker = sc.default_speaker()
        mic = sc.get_microphone(id=str(speaker.name), include_loopback=True)
        with mic.recorder(samplerate=self.samplerate, channels=1,
                          blocksize=self.blocksize) as rec:
            while not self._stop.is_set():
                data = rec.record(numframes=self.blocksize)
                mono = data[:, 0] if data.ndim > 1 else data
                pcm16 = (np.clip(mono, -1.0, 1.0) * 32767).astype(np.int16).tobytes()
                text, is_final = self.transcriber.accept(pcm16)
                if text:
                    self.on_text(text, is_final)
