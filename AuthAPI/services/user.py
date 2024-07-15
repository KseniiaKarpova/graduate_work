from functools import lru_cache
from uuid import UUID
from fastapi import Depends
from services import BaseService
from storages.user import UserStorage
from schemas.auth import UserUpdate, UserData
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import create_async_session
from exceptions import not_found, user_updated


class UserService(BaseService):
    def __init__(self, storage: UserStorage):
        self.storage = storage

    async def get_user(self, uuid: UUID):
        user, roles = await self.storage.with_roles(conditions={
            'uuid': uuid
        })
        if not user:
            raise not_found
        return UserData(
            uuid=user.uuid,
            email=user.email,
            name=user.name,
            surname=user.surname,
            roles=roles,
            is_superuser=user.is_superuser
        )

    async def get_users(self):
        users = await self.storage.get_all_users()
        if not users:
            raise not_found
        return users

    async def update_user(self, user_id: UUID, data: UserUpdate):
        await self.storage.update(
            conditions={
                "uuid": user_id,
            },
            values=data.dict(exclude_unset=True)
        )
        return user_updated


@lru_cache()
def get_user_service(
    session: AsyncSession = Depends(create_async_session)
) -> UserService:
    return UserService(storage=UserStorage(session=session))
