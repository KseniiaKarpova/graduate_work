import base64
import io
import os
import uuid
import wave

import numpy as np
import soundfile as sf
import torch
from core.logger import logger
from model import BaseModelManager, v1
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.utils.generic_utils import get_user_data_dir
from TTS.utils.manage import ModelManager


def init(set):
    if os.path.exists(set.path):
        logger.info("Loading custom model from " + set.path)
        model_path = set.path
    else:
        logger.info("Loading default model")

        logger.info("Downloading XTTS Model: " + set.name)
        ModelManager().download_model(set.name)
        model_path = os.path.join(get_user_data_dir("tts"), set.name.replace("/", "--"))
        logger.info("XTTS Model downloaded")

    logger.info("Loading XTTS")
    config = XttsConfig()
    config.load_json(os.path.join(model_path, "config.json"))
    v1.Model = Xtts.init_from_config(config)
    v1.get_model().load_checkpoint(config, checkpoint_dir=model_path, eval=True, use_deepspeed=False)
    # model.to(device)
    logger.info("XTTS Loaded.")
    v1.gpt_cond_latent, v1.speaker_embedding = v1.get_model().get_conditioning_latents('./model/v1/voices/roman.wav')
    v1.gpt_cond_latent = v1.get_gpt_cond_latent().cpu().squeeze().half().tolist()
    v1.speaker_embedding = v1.get_speaker_embedding().cpu().squeeze().half().tolist()
    logger.info("Done")


class XttsModelManager(BaseModelManager):

    def pre_process(self):
        pass

    def encode_audio_common(self,
                            frame_input,
                            encode_base64=True,
                            sample_rate=24000,
                            sample_width=2,
                            channels=1
                            ):
        """Return base64 encoded audio"""
        wav_buf = io.BytesIO()
        with wave.open(wav_buf, "wb") as vfout:
            vfout.setnchannels(channels)
            vfout.setsampwidth(sample_width)
            vfout.setframerate(sample_rate)
            vfout.writeframes(frame_input)

        wav_buf.seek(0)
        if encode_base64:
            b64_encoded = base64.b64encode(wav_buf.getbuffer()).decode("utf-8")
            return b64_encoded
        else:
            return wav_buf.read()

    def post_process(self, wav):
        """Post process the output waveform"""
        if isinstance(wav, list):
            wav = torch.cat(wav, dim=0)
        wav = wav.clone().detach().cpu().numpy()
        wav = wav[None, : int(wav.shape[0])]
        wav = np.clip(wav, -1, 1)
        wav = (wav * 32767).astype(np.int16)
        return wav

    def text_to_voice(self, text: str, language: str = 'ru'):
        speaker_embedding = torch.tensor(v1.speaker_embedding).unsqueeze(0).unsqueeze(-1)
        gpt_cond_latent = torch.tensor(v1.gpt_cond_latent).reshape((-1, 1024)).unsqueeze(0)
        out = v1.Model.inference(
            text,
            language,
            gpt_cond_latent,
            speaker_embedding,
        )
        wav = self.post_process(torch.tensor(out["wav"]))
        file_name = f'{uuid.uuid4()}.wav'
        sf.write(file_name, wav[0], 24000, subtype='PCM_24')
        return file_name
