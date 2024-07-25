from api.v1 import audio
from fastapi import APIRouter

v1_router = APIRouter(prefix='/v1')

v1_router.include_router(audio.router, tags=['audio'])
