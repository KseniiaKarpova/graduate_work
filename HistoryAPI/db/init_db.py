from beanie import init_beanie
from core.config import settings
from models.history import ChatHistory
from motor.motor_asyncio import AsyncIOMotorClient


async def init(*, client: AsyncIOMotorClient) -> None:
    await init_beanie(
        database=getattr(client, settings.mongodb.db_name),
        document_models=[ChatHistory],
    )
