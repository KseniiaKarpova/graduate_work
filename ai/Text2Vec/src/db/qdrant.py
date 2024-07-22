from qdrant_client import AsyncQdrantClient, models
from db import BaseVecDB
from exceptions import try_retry_after, return_bad_request, not_found, empty
from shemas import ResponseDB
from typing import List
from core.config import settings

THRESHOLD = settings.db.threshold or 0.9

client: AsyncQdrantClient = None

def get_client() -> AsyncQdrantClient:
    return client

def connect(host, port) -> AsyncQdrantClient:
    return  AsyncQdrantClient(url=f'http://{host}:{port}')

class QdrantDB(BaseVecDB):
    async def add(self, collection_name, docs, metadata, ids):
        try:
            ans = await get_client().add(
                collection_name=collection_name,
                documents=docs,
                metadata=metadata,
                ids=ids
            )

            return ans
        except ValueError:
            raise return_bad_request(f"I do not know anything about {collection_name} or Id is not a valid UUID. Check the correctness of the data being uploaded")
        except Exception:
            raise try_retry_after


    async def search(self, collection_name: str, query_text: str) -> ResponseDB:
        data = await self.search_many(collection_name, query_text, limit=1)
        return data[0]


    async def search_many(self, collection_name: str, query_text: str, limit: int=1) -> List[ResponseDB]:
        if query_text == '' or query_text == ' ':
            raise return_bad_request("Запрос пустой")

        try:
            data = await get_client().query(
                collection_name=collection_name,
                query_text=query_text,
                limit=limit
            )

        except ValueError:
            raise return_bad_request(f"I do not know anything about {collection_name}. Check the correctness of the data being uploaded")
        except Exception:
            raise try_retry_after

        ans = [ResponseDB(id=item.id,
                          score=item.score,
                          metadata=item.metadata) for item in data if item.score >= THRESHOLD]

        if len(ans) == 0:
            raise empty
        return ans