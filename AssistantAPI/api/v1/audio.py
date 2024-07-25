from fastapi import APIRouter, UploadFile, status, Depends
from core.handlers import require_access_token
from services.audio import get_service, AudioService
router = APIRouter(prefix="/audio")


@router.post("", status_code=status.HTTP_201_CREATED)
async def send_audio(
    service: AudioService = Depends(get_service)):
    return await service.proceed()
