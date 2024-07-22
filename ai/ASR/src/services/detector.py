from functools import lru_cache
from fastapi import Depends, UploadFile
import numpy as np
from typing import List
from services import MainDetector
from exceptions import file_error
from core.logger import logger

class Detector(MainDetector):

    async def file_to_frame(self, upload_file: UploadFile, frame_rate: int = 8000):
        try:
            audio_bytes = await upload_file.read()
            samples = np.frombuffer(audio_bytes, dtype=np.int16)
            samples = samples.astype(np.float32) / 32768

            return samples
        except Exception:
            raise file_error


class Service:

    def __init__(self, detector: Detector):
        self.detector = detector

    async def get_text(self, file: UploadFile):

        samples = await self.detector.file_to_frame(upload_file=file)
        text = self.detector.transcribe(samples)
        return {'text': text.strip()}

    async def get_text_long(self, file: UploadFile):
        samples = await self.detector.file_to_frame(upload_file=file)
        result = ''
        for start, stop in self.detector.vad_detect_2(samples):
            try:
                text = self.detector.transcribe(samples[start: stop], 8000).strip()
                logger.info(text)
                if len(text) > 2:
                    result = result + " " + text
            except Exception:
                pass

        return {'text': result.strip()}


    async def batch_text(self, files: List[UploadFile]):
        samples=[]
        for f in files:
            s = await self.detector.file_to_frame(upload_file=f)
            samples.append(s)
        return self.detector.batch_transcribe(samples)


@lru_cache(maxsize=128)
def detector_service(
    detector: Detector = Depends(Detector)
) -> Service:
    return Service(detector=detector)

