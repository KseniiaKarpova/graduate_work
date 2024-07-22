from storages import BaseStorage
from db import BaseVecDB
from shemas import ResponseDB
from shemas.entity import EntityModel
from services.translator import translation
from exceptions import created
from typing import List

class EntityStorage(BaseStorage):

    def __init__(self, database: BaseVecDB):
        self.database = database

    def transform(self, data: EntityModel):
        collection_name = data.collection_name
        docs = [translation(data.text)]
        data.metadata['text'] = data.text
        metadata = [data.metadata]
        ids = None
        return collection_name, docs, metadata, ids

    async def add(self, data: EntityModel):
        collection_name, docs, metadata, ids = self.transform(data)
        await self.database.add(collection_name, docs, metadata, ids)
        raise created

    async def search(self, collection_name: str, text: str)-> ResponseDB:
        result = await self.database.search(collection_name, text)
        return result

    async def search_many(self, collection_name: str, text: str, limit: int)-> List[ResponseDB]:
        result = await self.database.search_many(collection_name, text, limit)
        return result