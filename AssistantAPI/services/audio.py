from uuid import uuid4

from aiohttp import FormData
from core.config import settings
from core.handlers import require_access_token
from fastapi import Depends, UploadFile
from utils.request import HttpClient, get_http_client
from utils.detecter import Detector, get_detector


class AudioService:
    def __init__(self,
                 session: HttpClient,
                 audio: UploadFile,
                 token: str,
                 detector: Detector) -> None:
        self.session = session
        self.audio = audio
        self.token = token
        self.detector = detector

    async def proceed(self):
        await self.detector.check_file(upload_file=self.audio)
        audio_text = await self.speach_to_text()
        intent_text = await self.get_intents(text=audio_text)
        return await self.text_to_speach(text=intent_text)

    async def speach_to_text(self):
        form = await self.form()
        headers = await self.headers(with_file=True)
        response_data = await self.session.post(f"{settings.asr_api.path}", headers=headers, data=form, data_type='form')
        return response_data.get("text")

    async def get_intents(self, text: str):
        headers = await self.headers()
        response_data = await self.session.get(f"{settings.intent_api.path}/{text}", headers=headers)
        return response_data.get('text')

    async def text_to_speach(self, text: str):
        headers = await self.headers()
        return await self.session.get(f"{settings.tts_api.path}/{text}", headers=headers, to_json=True)

    async def save_file(self):
        form = await self.form()
        headers = await self.headers(with_file=True)
        response_data = await self.session.post(f"{settings.file_service.path}", headers=headers, data=form, data_type='form')
        return response_data.get("short_name")

    async def form(self) -> FormData:
        form = FormData()
        form.add_field('audio', self.audio.file, filename=self.audio.filename, content_type=self.audio.content_type)
        return form

    async def headers(self, with_file: bool = None):
        data = {
            "Authorization": f"Bearer {self.token}",
            "X-Request-Id": str(uuid4()),
            }
        if with_file:
            data.update({
                "Content-Disposition": f'attachment; filename="{self.audio.filename}";',
            })
        return data


def get_service(
        file: UploadFile,
        session: HttpClient = Depends(get_http_client),
        credentials=Depends(require_access_token),
        detector: Detector = Depends(get_detector),
) -> AudioService:
    _, token = credentials
    return AudioService(
        session=session, audio=file,
        token=token, detector=detector)
