from pydantic import BaseModel, Field, field_validator


class AnswerModel(BaseModel):
    text: str = Field(description='Текст')
    intent: str = Field(None, description='intent')
    entity: str = Field(None, description='entity')
    metadata: dict = Field(None, description='More info')
