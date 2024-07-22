import aiohttp


async def post_request(url: str, body: dict, head: dict):
    async with aiohttp.ClientSession() as session:
        response = await session.post(url=url,
                                      data=body,
                                      headers=head)
        result = await response.json()
        return result


async def get_request(url: str, head, params = None):
    async with aiohttp.ClientSession() as session:
        if params:
            response = await session.get(url=url, params=params, headers=head)
        else:
            response = await session.get(url=url, headers=head)
        result = await response.json()
        return result