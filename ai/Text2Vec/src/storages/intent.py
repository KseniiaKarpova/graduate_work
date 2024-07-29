from typing import List

from db import BaseVecDB
from exceptions import Created
from shemas import ResponseDB
from shemas.intent import IntentModel
from storages import BaseStorage


class IntentStorage(BaseStorage):

    def __init__(self, database: BaseVecDB):
        self.database = database
        self.collection_name = "Intents"

    def transform(self, data: IntentModel):
        collection_name = self.collection_name
        data.metadata['name'] = data.name
        metadata = [data.metadata] * len(data.texts)
        ids = data.ids
        return collection_name, data.texts, metadata, ids

    async def add(self, data: IntentModel):
        collection_name, docs, metadata, ids = self.transform(data)
        await self.database.add(collection_name, docs, metadata, ids)
        raise Created

    async def search(self, text: str) -> ResponseDB:
        result = await self.database.search(collection_name=self.collection_name,
                                            query_text=text)
        return result

    async def search_many(self, text: str, limit: int) -> List[ResponseDB]:
        result = await self.database.search_many(collection_name=self.collection_name,
                                                 query_text=text,
                                                 limit=limit)
        return result
