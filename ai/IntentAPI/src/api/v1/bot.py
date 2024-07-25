from services.facade import get_facade
from fastapi import APIRouter, Request, Depends
from core.handlers import require_access_token, JwtHandler
from models.bot import AnswerModel


router = APIRouter()


@router.get(
    "/ask/{text}"
)
async def ask(
    request: Request,
    text: str = "",
    jwt_handler: JwtHandler = Depends(require_access_token),
) -> AnswerModel:
    user = await jwt_handler.get_current_user()
    user_id = user.uuid
    result = await get_facade().ask(text, request)
    return result
