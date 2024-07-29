from core.handlers import JwtHandler, require_access_token
from fastapi import APIRouter, Depends, Request
from models.bot import AnswerModel
from services.facade import get_facade

router = APIRouter()


@router.get(
    "/ask/{text}"
)
async def ask(
    request: Request,
    text: str,
    jwt_handler: JwtHandler = Depends(require_access_token),
) -> AnswerModel:
    user = await jwt_handler.get_current_user()
    user_id = str(user.uuid)
    result = await get_facade().ask(text, user_id, request)
    await get_facade().log(result, user_id, request)
    return result
