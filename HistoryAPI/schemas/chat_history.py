from uuid import UUID
from pydantic import BaseModel, Field
from models.history import ChatHistory


class ChatHistoryDTo(BaseModel):
    user_id: UUID | None = Field(None)
    text: str | None = Field(None)
    file_id: str
    direction: str


class ChatHistoryList(BaseModel):
    items: list[ChatHistory]
    total: int
    page: int
    size: int
    pages: int
