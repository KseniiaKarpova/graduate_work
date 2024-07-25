from core.config import settings
from utils.request_api import post_request, get_request
from models.bot import ChatHistoryItem, ChatHistoryList
from fastapi import Request
from core.logger import logger


class HistoryServices:
    def __init__(self):
        self.url = settings.history.url

    async def save(self, item: ChatHistoryItem, request: Request):
        try:
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                "Authorization": request.headers.get('Authorization'),
                'X-Forwarded-For': request.headers.get('X-Forwarded-For') or request.headers.get('x-request-id'),
            'X-Request-Id': request.headers.get('X-Request-Id') or request.headers.get('x-request-id')
            }
            await post_request(url=self.url,
                               body=item.model_dump(mode='json'),
                               head=headers)
        except Exception as e:
            logger.error(e)


    async def get_last_entity(self, entity_type: str, user_id: str, request: Request):
        try:
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                "Authorization": request.headers.get('Authorization'),
                'X-Forwarded-For': request.headers.get('X-Forwarded-For') or request.headers.get('x-request-id'),
            'X-Request-Id': request.headers.get('X-Request-Id') or request.headers.get('x-request-id')
            }
            data: ChatHistoryList = await get_request(url=self.url,
                                     head=headers,
                                     params = {
                                         'user_id': user_id,
                                         'page': 1,
                                         'size': 20
                                        }
                                     )

            for item in data.get('items'):
                if item.get('entity') == entity_type:
                    return item.get('metadata')
        except Exception as e:
            logger.error(e)


