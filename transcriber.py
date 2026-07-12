import json

from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)


class Transcriber:
    def __init__(self, model_path, samplerate=16000):
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, samplerate)
        self.rec.SetWords(False)

    def accept(self, pcm_bytes):
        if self.rec.AcceptWaveform(pcm_bytes):
            result = json.loads(self.rec.Result())
            return result.get("text", ""), True
        partial = json.loads(self.rec.PartialResult())
        return partial.get("partial", ""), False
