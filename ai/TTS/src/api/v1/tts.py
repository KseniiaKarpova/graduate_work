import os

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from service.tts_service import TTSServices, get_tts_service

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
