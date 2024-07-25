from . import BaseService
from abc import  abstractmethod
from schemas.chat_history import ChatHistoryDTo
from storages.chat_history import ChatHistoryStorage
from models.history import ChatHistory
from uuid import UUID
from schemas.auth import JWTUserData


class BaseChatHistoryService(BaseService):
    def __init__(
            self,
            storage: ChatHistoryStorage) -> None:
        self.storage = storage

    @abstractmethod
    async def save_message(self):
        pass
    
    @abstractmethod
    async def remove_message(self):
        pass

class ChatHistoryService(BaseChatHistoryService):
    def __init__(self, storage: ChatHistoryStorage) -> None:
        super().__init__(storage)

    async def save_message(self, dto: ChatHistory, user: JWTUserData):
        if not dto.user_id:
            dto.user_id = user.uuid
        return await self.storage.create(dto=dto)

    async def remove_message(self, id: UUID):
        return await self.storage.delete(id=id)
    
    async def get_messages(self, user_id: UUID, params):
        return await self.storage.get_many(user_id=user_id, params=params)



def get_service():
    return ChatHistoryService(
        storage=ChatHistoryStorage()
    )
