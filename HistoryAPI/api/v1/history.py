from fastapi import APIRouter
from core.config import settings

router = APIRouter(prefix="/chat-history")

@router.get("")
async def read():
    pass


@router.post("")
async def create():
    pass
