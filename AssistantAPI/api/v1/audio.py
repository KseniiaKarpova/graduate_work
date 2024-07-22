from fastapi import APIRouter, UploadFile, HTTPException, status
from aiohttp import ClientSession, FormData
from core.config import settings
from core.handlers import require_access_token, JwtHandler

router = APIRouter(prefix="/audio")

@router.post("", status_code=status.HTTP_201_CREATED)
async def send_audio(
    file: UploadFile):
    async with ClientSession() as session:
        form = FormData()
        form.add_field('file',
                       file.file,
                       filename=file.filename,
                       content_type=file.content_type)
        headers = {"Content-Disposition": f'attachment; filename="{file.filename}"'}
        async with session.post(f"{settings.file_service.path}", headers=headers, data=form) as response:
            if response.status != 200:
                return HTTPException(status_code=response.status, detail=(await response.json())['detail'])
            response_json = await response.json()
        return response_json["short_name"]
