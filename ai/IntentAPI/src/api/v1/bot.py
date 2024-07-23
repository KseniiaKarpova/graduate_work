from service.facade import get_facade
from fastapi import APIRouter, Request


router = APIRouter()


@router.get(
    "/ask/{text}"
)
async def tts(
    request: Request,
    text: str = "",
):
    return get_facade().ask(text, request)