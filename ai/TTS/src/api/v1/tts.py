from service.tts_service import get_tts_service, TTSServices
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, BackgroundTasks
import os

router = APIRouter()



@router.get(
    "/text2speach/{text}",
    response_class=FileResponse,
    response_description="audio file"
)
async def tts(
    text: str = "",
    background_tasks: BackgroundTasks = BackgroundTasks(),
    tts_service: TTSServices = Depends(get_tts_service)
):
    audio = tts_service.text_to_voice(text)
    background_tasks.add_task(os.remove, audio)
    return FileResponse(audio)