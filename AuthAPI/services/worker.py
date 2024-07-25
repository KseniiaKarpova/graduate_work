from uuid import UUID

from services import BaseService


class BaseWorkerService(BaseService):
    async def send_email(self, user_id: UUID):
        pass
