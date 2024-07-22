from functools import lru_cache
from fastapi import Depends
from db import BaseVecDB
from db.qdrant import QdrantDB
from shemas import ResponseDB
from shemas.intent import IntentModel
from storages.intent import IntentStorage
from storages import BaseStorage
from typing import List

class IntentService:
    def __init__(self, storage):
        self.storage = storage

    async def add(self, data: IntentModel):
        return await self.storage.add(data)

    async def search(self, text: str) -> ResponseDB:
        result = await self.storage.search(text)
        return result

    async def search_many(self, text: str, limit: int) -> List[ResponseDB]:
        result = await self.storage.search_many(text, limit)
        return result


@lru_cache()
def get_intent_service(
    database: QdrantDB = Depends(QdrantDB)
) -> IntentService:
    storage = IntentStorage(database)
    return IntentService(storage)