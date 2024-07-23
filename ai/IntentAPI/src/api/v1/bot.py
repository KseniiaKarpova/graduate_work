from services.facade import get_facade
from fastapi import APIRouter, Request


router = APIRouter()


@router.get(
    "/ask/{text}"
)
async def tts(
    request: Request,
    text: str = "",
):
    result = await get_facade().ask(text, request)
    return result