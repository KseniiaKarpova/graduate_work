from uuid import UUID
from beanie import Document
from pydantic import Field, BaseModel
from models import BaseMixin
from enum import Enum


class MessageDirection(str, Enum):
    SENT = "sent"
    RECEIVED = "received"


class MetaData(BaseModel):
    document: str
    films_cont: int
    id: UUID
    name: str


class ChatHistory(BaseMixin, Document):
    user_id: UUID
    text: str | None = Field(None)
    direction: MessageDirection = Field(...)
    intent: str | None = Field(None)
    entity: str | None = Field(None)
    metadata: MetaData | None = Field(None)

    class Settings:
        name = "chat_history"
        use_state_management = True
