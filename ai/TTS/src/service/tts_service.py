from model.v2.manager import VoskModelManager
from model import BaseModelManager
from functools import lru_cache
from fastapi import Depends


class TTSServices:

    def __init__(self, model_manger: BaseModelManager):
        self.model_manger = model_manger

    def text_to_voice(self, text: str):
        return self.model_manger.text_to_voice(text=text)


@lru_cache()
def get_tts_service(
    model_manger: BaseModelManager = Depends(VoskModelManager),
) -> TTSServices:
    return TTSServices(model_manger)