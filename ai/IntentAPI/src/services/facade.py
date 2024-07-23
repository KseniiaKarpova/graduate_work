from utils.request_api import post_request, get_request
import yaml
import exceptions
from fastapi import Request, status
from fastapi.responses import ORJSONResponse
import random

facade = None

def get_facade():
    return facade

class Facade:

    def __init__(self,
                 url: str,
                 file: str):
        self.url = url
        with open(file) as fh:
            self.conf = yaml.load(fh, Loader=yaml.FullLoader)
        print(self.conf)

    async  def create(self):
        for item in self.conf.get('intents'):
            json_data = {
                'name': item.get('name'),
                'texts': item.get('query'),
                'ids': [i for i in range(len(item.get('query')))],
                'metadata': {},
            }
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Forwarded-For': 'Intent',
                'X-Request-Id': str(item.get('id'))
            }
            response = await post_request(self.url, head=headers, body=json_data)
            print(response)

    async def ask(self, text: str, request: Request):
        return text

    async def get_class(self, text: str, request: Request):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Forwarded-For': request.headers.get('X-Forwarded-For'),
            'X-Request-Id': request.headers.get('X-Request-Id')
        }
        try:
            response = await get_request(self.url, head=headers, params={'text': text})
            print(response)
        except Exception:
            raise ORJSONResponse(
            status_code=status.HTTP_204_NO_CONTENT, content={
                    'text': random.choice(self.conf.get('no_answer'))
                }
            )






