from fastapi import APIRouter, Depends, status
from services.audio import AudioService, get_service


router = APIRouter(prefix="/audio")


@router.post("", status_code=status.HTTP_201_CREATED)
async def send_audio(
        service: AudioService = Depends(get_service)):
    return await service.proceed()
