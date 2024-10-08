from db import AbstractStorage
from exceptions import FileAlreadyExistError, FileNotFoundError
from models.file_db import FileDbModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

engine = None
async_session = None


async def get_engine():
    return engine


async def get_session() -> AsyncSession:
    async with async_session() as session:
        return session


class PostgresStorage(AbstractStorage):
    async def save(self, data, path):
        object = FileDbModel(
            path_in_storage=path,
            filename=data.get('filename'),
            size=data.get('size'),
            file_type=data.get('file_type'),
            short_name=data.get('short_name')
        )
        await self.insert_object(object)

    async def insert_object(self, object) -> None:
        try:
            session = await get_session()
            async with session.begin():
                session.add(object)
        except IntegrityError:
            raise FileAlreadyExistError

    async def get(self, short_name):
        try:
            session = await get_session()
            result = await session.execute(select(FileDbModel.path_in_storage, FileDbModel.filename).
                                           where(FileDbModel.short_name == short_name).
                                           limit(1))
            for i in result:
                return i
        except Exception:
            raise FileNotFoundError
