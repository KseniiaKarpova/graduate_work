from typing import List

from db import BaseVecDB
from exceptions import created
from services.translator import translation
from shemas import ResponseDB
from shemas.entity import EntityModel
from storages import BaseStorage


class EntityStorage(BaseStorage):

    def __init__(self, database: BaseVecDB):
        self.database = database

    def trans(self, data: dict):
        for key, val in data.items():
            if isinstance(val, str):
                data[key] = translation(val)
        return data

    def transform(self, data: EntityModel):
        collection_name = data.collection_name
        docs = [translation(data.text)]
        metadata = [self.trans(data.metadata)]
        ids = None
        return collection_name, docs, metadata, ids

    async def add(self, data: EntityModel):
        collection_name, docs, metadata, ids = self.transform(data)
        await self.database.add(collection_name, docs, metadata, ids)
        raise created

    async def search(self, collection_name: str, text: str) -> ResponseDB:
        result = await self.database.search(collection_name, text)
        return result

    async def search_many(self, collection_name: str, text: str, limit: int) -> List[ResponseDB]:
        result = await self.database.search_many(collection_name, text, limit)
        return result
