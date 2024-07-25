# from core.handlers import JwtHandler, require_access_token
from fastapi import APIRouter, Depends
from services.intent import IntentService, get_intent_service
from shemas.intent import IntentModel

router = APIRouter()


@router.post("/")
async def add(
        data: IntentModel,
        service: IntentService = Depends(get_intent_service),
        # jwt_handler: JwtHandler = Depends(require_access_token)
):
    return await service.add(data)


@router.get("/")
async def search(
        text: str,
        service: IntentService = Depends(get_intent_service),
        # jwt_handler: JwtHandler = Depends(require_access_token)
):
    return await service.search(text)


@router.get("/{limit}/")
async def search_many(
        limit: int,
        text: str,
        service: IntentService = Depends(get_intent_service),
        # jwt_handler: JwtHandler = Depends(require_access_token)
):
    return await service.search_many(text, limit)
