from fastapi import APIRouter

from api.v1 import chat_history


v1_router = APIRouter(prefix='/v1')

v1_router.include_router(chat_history.router, tags=['chat_history'])
