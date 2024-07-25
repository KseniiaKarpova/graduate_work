from aiohttp import ClientSession, ClientResponse, FormData, ClientConnectionError
from typing import Generator
from fastapi import HTTPException


# Dependency to provide an aiohttp session
async def get_http_client():
    async with ClientSession() as session:
        converter = DataConverter()
        client = HttpClient(converter, session=session)
        yield client


class DataConverter:
    @staticmethod
    def to_form_data(data: dict) -> FormData:
        form = FormData()
        for key, value in data.items():
            form.add_field(key, value)
        return form

    @staticmethod
    def to_json(data: dict) -> dict:
        return data


class HttpClient:
    def __init__(self, converter: DataConverter, session: ClientSession) -> None:
        self._session: ClientSession = session or ClientSession()
        self._converter = converter

    async def post(self, url: str, headers: dict = None, data: dict = None, data_type: str = 'json') -> ClientResponse:
        if data_type == 'json':
            data = self._converter.to_json(data)
        async with self._session.post(url, headers=headers, data=data if data_type == 'form' else None, json=data if data_type == 'json' else None) as response:
            return await self._handle_response(response)

    async def get(self, url: str, headers: dict = None, params: dict = None, to_json: bool = True):
        async with self._session.get(url, headers=headers, params=params) as response:
            if not to_json:
                return response
            return await self._handle_response(response)

    async def _handle_response(self, response: ClientResponse):
        if response.status != 200:
            try:
                response_data = await response.json()
            except Exception:
                response_data = {"detail": "Unknown error"}
            raise HTTPException(status_code=response.status, detail=response_data.get('detail', 'Unknown error'))
        return await response.json() if response.content_type == 'application/json' else await response.text()
