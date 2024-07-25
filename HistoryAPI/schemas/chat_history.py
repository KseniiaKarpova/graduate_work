from uuid import UUID
from pydantic import BaseModel, Field
from models.history import ChatHistory, MetaData


class ChatHistoryDTo(BaseModel):
    user_id: UUID | None = Field(None)
    text: str | None = Field(None)
    direction: str
    intent: str
    entity: str | None = Field(None)
    metadata: MetaData | None = Field(None)



class ChatHistoryList(BaseModel):
    items: list[ChatHistory]
    total: int
    page: int
    size: int
    pages: int
