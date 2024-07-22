from pydantic import BaseModel, Field, field_validator


class ScriptModel(BaseModel):
    text: str = Field(description='Текст')
    metadata: dict = Field(description='More info')

