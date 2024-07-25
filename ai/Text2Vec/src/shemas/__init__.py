from pydantic import BaseModel, Field


class ResponseDB(BaseModel):
    id: str | int = Field(description='Item ID')
    score: float = Field(description='Score (cosine)')
    metadata: dict = Field(description='More info')
