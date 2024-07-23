from utils.request_api import post_request, get_request
import yaml
import exceptions
from nlu.map_functions import map_func
from nlu.normalize import number_to_words, inflect_with_num
from functools import lru_cache
from fastapi import HTTPException, Request, status
from core.config import settings
import random
from typing import List


facade = None
pars = '[type]'
intent = 'intent'
entity = 'entity'
api = settings.cinema.url

@lru_cache
def get_facade():
    return facade

class Facade:

    def __init__(self,
                 url: str,
                 file: str):
        self.url = url
        with open(file) as fh:
            self.conf = yaml.load(fh, Loader=yaml.FullLoader)

    async  def create(self):
        last = 0
        for item in self.conf.get('intents'):
            json_data = {
                'name': item.get('name'),
                'texts': item.get('query'),
                'ids': [i+last for i in range(len(item.get('query')))],
                'metadata': {},
            }
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Forwarded-For': 'Intent',
                'X-Request-Id': str(item.get('id'))
            }
            response = await post_request(self.url.replace(pars, intent), head=headers, body=json_data)
            last = last + len(item.get('query'))
            print(item.get('query'), response)

    async def ask(self, text: str, request: Request):
        cl = await self.search_class(text, request)
        if not cl:
            return random.choice(self.conf.get('no_answer'))
        else:
            data = self.get_entity(cl)
            id = await self.search_entity(data.get('entity'), request)
            if not id:
                return random.choice(self.conf.get('no_answer'))
            else:
                cinema_data = await self.search_data(id, data.get('uri'), request)
                print('cinema_data', cinema_data)
                if cinema_data:
                    res = self.refactor_cinema(data.get('script'), cinema_data)
                    print('res', res)
                    return self.refactor_answer(data.get('answer'), res)
                else:
                    return random.choice(self.conf.get('no_answer'))

    def refactor_cinema(self, script: List[str], data):
        last = data[0]
        i = 0
        while i < len(script):
            d = map_func(last)
            if not d:
                last = data.get(d)
            else:
                return d

    def refactor_answer(self, answer: str, data):
        return answer
        #if isinstance(data, int):
        #    pass
            #data =

    def get_entity(self, text: str):
        for item in self.conf.get('intents'):
            if text == item.get('name'):
                return item

    async def search_data(self, id: str, path: str, request: Request):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Forwarded-For': request.headers.get('X-Forwarded-For'),
            'X-Request-Id': request.headers.get('X-Request-Id')
        }
        try:
            response = await get_request(api + path.replace('{id}', id), head=headers)
            return response
        except Exception:
            return None

    async def search_entity(self, text: str, request: Request):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Forwarded-For': request.headers.get('X-Forwarded-For'),
            'X-Request-Id': request.headers.get('X-Request-Id')
        }
        try:
            response = await get_request(self.url.replace(pars, entity), head=headers, params={'text': text})
            return response.get('metadata').get('id')
        except Exception:
            return None

    async def search_class(self, text: str, request: Request):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Forwarded-For': request.headers.get('X-Forwarded-For'),
            'X-Request-Id': request.headers.get('X-Request-Id')
        }
        try:
            response = await get_request(self.url.replace(pars, intent), head=headers, params={'text': text})
            return response.get('metadata').get('name')
        except Exception:
            return  None

