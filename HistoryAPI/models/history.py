from uuid import UUID
from beanie import Document
from pydantic import Field
from models import BaseMixin
from enum import Enum


class MessageDirection(str, Enum):
    SENT = "sent"
    RECEIVED = "received"


class ChatHistory(BaseMixin, Document):
    user_id: UUID
    text: str | None = Field(None)
    file_id: str | None = Field(None)
    direction: MessageDirection = Field(...)

    class Settings:
        name = "chat_history"
        use_state_management = True
