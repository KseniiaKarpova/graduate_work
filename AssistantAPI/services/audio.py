from core.config import settings
from aiohttp import ClientSession, FormData
from utils.request import get_http_client, HttpClient
from fastapi import Depends, UploadFile
from core.handlers import require_access_token


class AudioService:
    def __init__(self, session: HttpClient, audio: UploadFile, token: str) -> None:
        self.session = session
        self.audio = audio
        self.token = token

    async def proceed(self):
        audio_text = await self.speach_to_text()
        intent_text = await self.get_intents(text=audio_text)
        return await self.text_to_speach(text=intent_text)

    async def speach_to_text(self):
        form = await self.form()
        headers = await self.headers()
        response_data = await self.session.post(f"{settings.asr_api.path}", headers=headers, data=form, data_type='form')
        return response_data.get("text")

    async def get_intents(self, text: str):
        headers = await self.headers()
        response_data = await self.session.get(f"{settings.intent_api.path}/{text}", headers=headers)
        return response_data.get('text')

    async def text_to_speach(self, text: str):
        headers = await self.headers()
        response_data = await self.session.get(f"{settings.tts_api.path}/{text}", headers=headers)
        return response_data

    async def save_file(self):
        form = await self.form()
        headers = await self.headers()
        response_data = await self.session.post(f"{settings.file_service.path}", headers=headers, data=form, data_type='form')
        return response_data.get("short_name")

    async def form(self) -> FormData:
        return FormData().add_field('file', self.audio.file, filename=self.audio.filename, content_type=self.audio.content_type)

    async def headers(self):
        return {
            "Content-Disposition": f'attachment; filename="{self.audio.filename}";',
            "Authorization": f"Bearer {self.token}"
        }


def get_service(
        file: UploadFile,
        session: HttpClient = Depends(get_http_client),
        credentials=Depends(require_access_token),
        ) -> AudioService:
    jwt_handler, token = credentials
    return AudioService(session=session, audio=file, token=token)
