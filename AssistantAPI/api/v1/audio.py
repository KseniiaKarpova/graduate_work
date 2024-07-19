from fastapi import APIRouter, UploadFile, Response
from aiohttp import ClientSession, FormData
from core.config import settings

router = APIRouter(prefix="/audio")

@router.post("/upload")
async def upload_file(file: UploadFile):
    async with ClientSession() as session:
        form = FormData()
        form.add_field('file',
                       file.file,
                       filename=file.filename,
                       content_type=file.content_type)
        headers = {"Content-Disposition": f'attachment; filename="{file.filename}"'}
        async with session.post(f"{settings.file_service.path}", headers=headers, data=form) as response:
            if response.status != 200:
                return Response(status_code=response.status, content="Failed to upload to external API")
            response_json = await response.json()
        print(response_json)
        return response_json["short_name"]
