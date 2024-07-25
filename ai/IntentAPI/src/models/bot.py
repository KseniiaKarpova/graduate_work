from pydantic import BaseModel, Field


class AnswerModel(BaseModel):
    query: str = Field(description='Текст запроса')
    text: str = Field(description='Текст ответа')
    intent: str | None = Field(None, description='intent')
    entity: str | None = Field(None, description='entity')
    metadata: dict | None = Field(None, description='More info')


class ChatHistoryItem(AnswerModel):
    user_id: str


class ChatHistoryList(BaseModel):
    items: list[ChatHistoryItem]
    total: int
    page: int
    size: int
    pages: int
