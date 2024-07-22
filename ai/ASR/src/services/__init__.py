import numpy as np
from typing import List, Any
from services.recognizer import get_recognizer
import webrtcvad


class MainDetector:
    def __init__(self):
        self.recognizer = get_recognizer()

    def transcribe(self, samples, sample_rate: int=8000):
        try:
            s = self.recognizer.create_stream()
            s.accept_waveform(sample_rate, samples)
            self.recognizer.decode_stream(s)
            return s.result.text
        except Exception:
            pass

    def batch_transcribe(self, samples: List[Any], sample_rate: int=8000):
        streams = []
        for sam in samples:
            s = self.recognizer.create_stream()
            s.accept_waveform(sample_rate, sam)
            streams.append(s)

        self.recognizer.decode_streams(streams)
        results = [{"text": s.result.text} for s in streams]
        return results


    def frame_generator(self, audio, frame_duration_ms: int = 30,  sample_rate: int = 8000):
        """Generates audio frames from PCM audio data.

        Args:
            frame_duration_ms: The desired frame duration in milliseconds.
            audio: The PCM data.
            sample_rate: The sample rate
        """
        n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
        offset = 0
        while offset + n < len(audio):
            yield (offset, offset + n)
            offset += n

    def vad_detect_2(self, audio, sample_rate: int = 8000):
        self.vad = webrtcvad.Vad(2)
        s = 0
        size = 144000 # 480*300
        for idx, (start, end) in enumerate(self.frame_generator(audio)):
            if start >= s:
                frame = audio[start: end]
                if frame.dtype.kind == 'f':
                    # convert to int16
                    frame = np.array([int(s * 32768) for s in frame])
                    # bound
                    frame[frame > 32767] = 32767
                    frame[frame < -32768] = -32768
                is_speech = self.vad.is_speech(frame, sample_rate)
                if is_speech:
                    s = start+size
                    yield start, start+size