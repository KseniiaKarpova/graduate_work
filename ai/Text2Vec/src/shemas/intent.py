from typing import List

from pydantic import BaseModel, Field


class IntentModel(BaseModel):
    name: str = Field(description='Name of Intent')
    texts: List[str] = Field(description='Текст')
    ids: List[int] = Field(description='Индексы')
    metadata: dict = Field({}, description='More info')
