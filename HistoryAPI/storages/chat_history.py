from uuid import UUID

import pymongo
from exceptions import already_exists, deleted
from fastapi_pagination.ext.beanie import paginate
from models.history import ChatHistory, Document
from pymongo.errors import DuplicateKeyError
from storages import BaseStorage


class ChatHistoryStorage(BaseStorage):
    document: Document = ChatHistory

    async def create(self, dto: ChatHistory):
        try:
            return await dto.create()
        except DuplicateKeyError:
            raise already_exists

    async def delete(self, id: UUID):
        await self.document.find({'_id': id}).delete()
        return deleted

    async def get_many(self, params, **kwargs):
        return await paginate(ChatHistory.find_many(kwargs).sort([("created_at", pymongo.DESCENDING)]), params=params)
