from functools import lru_cache
from typing import List

import numpy as np
from core.logger import logger
from core import settings
from exceptions import BigFileError, FileError
from fastapi import Depends, UploadFile
from services import MainDetector


class Detector(MainDetector):

    async def file_to_frame(self, upload_file: UploadFile):
        if upload_file.size > settings.core.max_size:
            raise BigFileError

        if not (upload_file.content_type in settings.core.valid_content_type):
            raise FileError
        try:
            audio_bytes = await upload_file.read()
            samples = np.frombuffer(audio_bytes, dtype=np.int16)
            return samples.astype(np.float32) / settings.core.max_val

        except ValueError:
            raise FileError
        except Exception as e:
            logger.error(e)
            raise FileError


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
                text = self.detector.transcribe(samples[start: stop], settings.core.recommended_sample_rate).strip()
                logger.info(text)
                if len(text) > 2:
                    result = result + " " + text
            except Exception as e:
                logger.error("Can`t transcribe sample. " + str(e))

        return {'text': result.strip()}

    async def batch_text(self, files: List[UploadFile]):
        samples = []
        for f in files:
            s = await self.detector.file_to_frame(upload_file=f)
            samples.append(s)
        return self.detector.batch_transcribe(samples)


@lru_cache(maxsize=128)
def detector_service(
    detector: Detector = Depends(Detector)
) -> Service:
    return Service(detector=detector)
