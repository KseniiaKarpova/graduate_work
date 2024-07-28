from exceptions import ServerError
from fastapi import APIRouter, Depends, UploadFile
from services.detector import Service, detector_service

router = APIRouter()


@router.post(
    "/transcript/1/long",
    response_description="Transcript text from long mono audio",
    summary="Get transcript from short long audio file",
    description="Транскибирование длинных одноканальных аудио",
)
async def transcript_long(
        detector_service: Service = Depends(detector_service),
        audio: UploadFile = None,
):
    res = await detector_service.get_text_long(file=audio)
    if not res:
        raise ServerError
    return res
