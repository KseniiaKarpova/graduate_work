from uuid import UUID
from beanie import Document
from pydantic import Field, BaseModel
from models import BaseMixin


class ChatHistory(BaseMixin, Document):
    user_id: UUID
    query: str | None = Field(None)
    text: str | None = Field(None)
    intent: str | None = Field(None)
    entity: str | None = Field(None)
    metadata: dict | None = Field(None)

    class Settings:
        name = "chat_history"
        use_state_management = True
