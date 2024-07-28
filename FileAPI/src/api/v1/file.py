from core.handlers import require_access_token
from exceptions import FileNotFoundError
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from models.file import File
from services.file import FileService, get_file_service

router = APIRouter()


@router.post(
    "/",
    response_model=File,
    response_description="Upload file",
    summary="return short_name of file",
    description="",
)
async def upload_file(
        file: UploadFile,
        file_service: FileService = Depends(get_file_service),
        credentials=Depends(require_access_token)
) -> File:
    jwt_handler, token = credentials
    await jwt_handler.get_current_user()
    return await file_service.upload(file)


@router.get(
    "/download-stream/{name}",
    response_description="stream video file",
    description="File searching",
    summary="stream video file",
)
async def download_file(
    file_service: FileService = Depends(get_file_service),

    name: str = "",
) -> StreamingResponse:
    films = await file_service.download_stream(name)
    if not films:
        raise FileNotFoundError
    return films


@router.get(
    "/download/{name}",
    response_class=FileResponse,
    response_description="file",
    description="File searching",
    summary="stream audio file",
)
async def download_file_audio(
    file_service: FileService = Depends(get_file_service),
    name: str = "",
) -> FileResponse:
    films = await file_service.download(name)
    if not films:
        raise FileNotFoundError
    return films
