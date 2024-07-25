from functools import lru_cache
from typing import List

from db.qdrant import QdrantDB
from fastapi import Depends
from shemas import ResponseDB
from shemas.entity import EntityModel
from storages import BaseStorage
from storages.entity import EntityStorage


class EntityService:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    async def add(self, data: EntityModel):
        return await self.storage.add(data)

    async def search(self, collection_name: str, text: str) -> ResponseDB:
        result = await self.storage.search(collection_name, text)
        return result

    async def search_many(self, collection_name: str, text: str, limit: int) -> List[ResponseDB]:
        result = await self.storage.search_many(collection_name, text, limit)
        return result


@lru_cache()
def get_entity_service(
    database: QdrantDB = Depends(QdrantDB)
) -> EntityService:
    storage = EntityStorage(database)
    return EntityService(storage)
