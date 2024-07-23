from fastapi import APIRouter, Depends, UploadFile
from exceptions import file_not_found, server_error
from models.file import File
from services.file import FileService, get_file_service
from fastapi.responses import StreamingResponse

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
) -> File:
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
    films = await file_service.download(name)
    if not films:
        raise file_not_found
    return films
