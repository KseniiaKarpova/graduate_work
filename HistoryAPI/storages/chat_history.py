from models.history import ChatHistory, Document
from storages import BaseStorage
from uuid import UUID
from exceptions import already_exists, deleted
from pymongo.errors import DuplicateKeyError
from schemas.chat_history import ChatHistoryDTo
from fastapi_pagination.ext.beanie import paginate


class ChatHistoryStorage(BaseStorage):
    document: Document = ChatHistory

    async def create(self, dto: ChatHistoryDTo):
        try:
            return await ChatHistory(
                user_id=dto.user_id,
                text=dto.text,
                file_id=dto.file_id,
                direction=dto.direction
            ).create()
        except DuplicateKeyError:
            raise already_exists

    async def delete(self, id: UUID):
        await self.document.find({'_id': id}).delete()
        return deleted

    async def get_many(self, params, **kwargs):
        return await paginate(ChatHistory.find_many(kwargs), params=params)
