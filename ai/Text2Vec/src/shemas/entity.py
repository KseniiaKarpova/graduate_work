from pydantic import BaseModel, Field, field_validator
import uuid

class EntityModel(BaseModel):
    collection_name: str = Field(description='Название коллекции')
    text: str = Field(description='Текст')
    metadata: dict = Field(description='More info')