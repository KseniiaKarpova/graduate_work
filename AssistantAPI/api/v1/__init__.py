from fastapi import APIRouter

from api.v1 import audio


v1_router = APIRouter(prefix='/v1')

v1_router.include_router(audio.router, tags=['audio'])
