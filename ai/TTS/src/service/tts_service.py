import os
from functools import lru_cache

import exceptions
from core.config import settings
from fastapi import Depends, Request
from model import BaseModelManager
from model.v2.manager import VoskModelManager
from utils import upload_files


class TTSServices:

    def __init__(self, model_manger: BaseModelManager):
        self.model_manger = model_manger

    def text_to_voice(self, text: str):
        return self.model_manger.text_to_voice(text=text)

    async def save_file(self, path_file, request: Request):
        try:
            response_data = await upload_files(path_file, settings.file.path, request)
            return {'short_name': response_data.get("short_name")}
        except Exception:
            os.remove(path_file)
            raise exceptions.try_retry_after


@lru_cache()
def get_tts_service(
    model_manger: BaseModelManager = Depends(VoskModelManager),
) -> TTSServices:
    return TTSServices(model_manger)
