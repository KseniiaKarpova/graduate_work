from uuid import UUID

from models.history import ChatHistory
from pydantic import BaseModel, Field


class ChatHistoryDTo(BaseModel):
    user_id: UUID | None = Field(None)
    query: str | None = Field(None)
    text: str | None = Field(None)
    intent: str | None = Field(None)
    entity: str | None = Field(None)
    metadata: dict | None = Field(None)


class ChatHistoryList(BaseModel):
    items: list[ChatHistory]
    total: int
    page: int
    size: int
    pages: int
