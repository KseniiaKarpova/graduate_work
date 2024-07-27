from typing import Any, List

import numpy as np
import webrtcvad
from services.recognizer import get_recognizer
from core import settings


class MainDetector:
    def __init__(self):
        self.recognizer = get_recognizer()

    def transcribe(self,
                   samples,
                   sample_rate: int = settings.core.recommended_sample_rate):
        try:
            s = self.recognizer.create_stream()
            s.accept_waveform(sample_rate, samples)
            self.recognizer.decode_stream(s)
            return s.result.text
        except Exception:
            pass

    def batch_transcribe(self,
                         samples: List[Any],
                         sample_rate: int = settings.core.recommended_sample_rate):
        streams = []
        for sam in samples:
            s = self.recognizer.create_stream()
            s.accept_waveform(sample_rate, sam)
            streams.append(s)

        self.recognizer.decode_streams(streams)
        results = [{"text": s.result.text} for s in streams]
        return results

    def frame_generator(self,
                        audio,
                        frame_duration_ms: int = 30,
                        sample_rate: int = settings.core.recommended_sample_rate):
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

    def vad_detect_2(self,
                     audio,
                     sample_rate: int = settings.core.recommended_sample_rate):
        self.vad = webrtcvad.Vad(settings.vad.aggressiveness_mode)
        s = 0
        size = settings.vad.split_size
        for idx, (start, end) in enumerate(self.frame_generator(audio)):
            if start >= s:
                frame = audio[start: end]
                if frame.dtype.kind == 'f':
                    # convert to int16
                    frame = np.array([int(s * settings.core.max_val) for s in frame])
                    # bound
                    frame[frame > settings.core.max_val] = settings.core.max_val
                    frame[frame < -settings.core.max_val] = -settings.core.max_val
                is_speech = self.vad.is_speech(frame, sample_rate)
                if is_speech:
                    s = start + size
                    yield start, start + size
