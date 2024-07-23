import aiohttp
from fastapi import status
from fastapi.responses import ORJSONResponse

def check_header(headers):
    user = headers.get('X-Forwarded-For')
    if not user:
        raise ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={
                'detail': 'X-Forwarded-For is required'})

    request_id = headers.get('X-Request-Id')
    if not request_id:
        raise ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={
                'detail': 'X-Request-Id is required'})

async def post_request(url: str, body: dict, head: dict):
    check_header(head)
    async with aiohttp.ClientSession() as session:
        response = await session.post(url=url,
                                      data=body,
                                      headers=head)
        result = await response.json()
        return result


async def get_request(url: str, head, params = None):
    check_header(head)
    async with aiohttp.ClientSession() as session:
        if params:
            response = await session.get(url=url, params=params, headers=head)
        else:
            response = await session.get(url=url, headers=head)
        result = await response.json()
        return result