import uuid
from core.logger import logger
from model import BaseModelManager
from vosk_tts import Model, Synth
from model import v2

def init(model_name):
    model = Model(model_name=model_name)
    v2.Model = Synth(model)
    logger.info("Done")


class VoskModelManager(BaseModelManager):

    def pre_process(self):
        pass

    def post_process(self, wav):
        pass

    def text_to_voice(self, text: str):
        file_name = f'{uuid.uuid4()}.wav'
        v2.Model.synth(text, file_name, speaker_id=2)
        return file_name