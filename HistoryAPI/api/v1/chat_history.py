from uuid import UUID

from core.handlers import JwtHandler, require_access_token
from fastapi import APIRouter, Body, Depends, status
from fastapi_pagination import Params
from models.history import ChatHistory
from schemas.chat_history import ChatHistoryDTo, ChatHistoryList
from services.chat_history import ChatHistoryService, get_service

router = APIRouter(prefix="/chat-history")


@router.get("", status_code=status.HTTP_200_OK)
async def read(
    user_id: UUID | None = None,
    jwt_handler: JwtHandler = Depends(require_access_token),
    service: ChatHistoryService = Depends(get_service),
    params: Params = Depends()
):
    user = await jwt_handler.get_current_user()
    if not user_id:
        user_id = user.uuid
    return await service.get_messages(user_id=user_id, params=params)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    jwt_handler: JwtHandler = Depends(require_access_token),
    service: ChatHistoryService = Depends(get_service),
    dto: ChatHistory = Body(),
):
    user = await jwt_handler.get_current_user()
    return await service.save_message(dto=dto, user=user)
