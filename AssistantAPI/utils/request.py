from aiohttp import ClientSession, ClientResponse, FormData, ClientConnectionError
from fastapi import HTTPException, status


# Dependency to provide an aiohttp session
async def get_http_client():
    converter = DataConverter()
    async with HttpClient(converter) as client:
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
    def __init__(self, converter: DataConverter) -> None:
        self._session: ClientSession = None
        self._converter = converter

    async def __aenter__(self) -> 'HttpClient':
        self._session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self._session.close()

    async def post(self, url: str, headers: dict = None, data: dict = None, data_type: str = 'json') -> ClientResponse:
        if data_type == 'json':
            data = self._converter.to_json(data)
        async with self._session.post(url, headers=headers, data=data if data_type == 'form' else None, json=data if data_type == 'json' else None) as response:
            response_data = await response.json()
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=response_data.get('detail', 'Unknown error'))
            return response_data


    async def get(self, url: str, headers: dict = None, params: dict = None):
        async with self._session.get(url, headers=headers, params=params) as response:
            response_data = await response.json()
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=response_data.get('detail', 'Unknown error'))
            return response_data
