from fastapi import APIRouter, Depends
from services.entity import EntityService, get_entity_service
from shemas.entity import EntityModel

router = APIRouter()


@router.post("/")
async def add(
        data: EntityModel,
        service: EntityService = Depends(get_entity_service),
        # jwt_handler: JwtHandler = Depends(require_access_token)
):
    return await service.add(data)


@router.get("/")
async def search(
        collection_name: str,
        text: str,
        service: EntityService = Depends(get_entity_service),
        # jwt_handler: JwtHandler = Depends(require_access_token)
):
    return await service.search(collection_name, text)


@router.get("/{limit}/")
async def search_many(
        limit: int,
        collection_name: str,
        text: str,
        service: EntityService = Depends(get_entity_service),
        # jwt_handler: JwtHandler = Depends(require_access_token)
):
    return await service.search_many(collection_name, text, limit)
