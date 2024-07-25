from service.tts_service import get_tts_service, TTSServices
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, BackgroundTasks, Request
import os
from schemas.file import File


router = APIRouter()


@router.get(
    "/text2speach/{text}",
    response_description="data from File Service"
)
async def tts(
    request: Request,
    text: str = "",
    background_tasks: BackgroundTasks = BackgroundTasks(),
    tts_service: TTSServices = Depends(get_tts_service),
):
    audio = tts_service.text_to_voice(text)
    result = await tts_service.save_file(audio, request)
    background_tasks.add_task(os.remove, audio)
    print(result)
    return result