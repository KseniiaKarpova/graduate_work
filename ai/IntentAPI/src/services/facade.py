from utils.request_api import post_request, get_request
import yaml
from models.bot import AnswerModel
from nlu.normalize import number_to_words, inflect_with_num, LCS
from functools import lru_cache
from fastapi import HTTPException, Request, status
from core.config import settings
import random
import re


facade = None
pars = '[type]'
intent = 'intent'
entity = 'entity'
api = settings.cinema.url

@lru_cache
def get_facade():
    return facade

class Facade:
    pattern = re.compile("\((.*)\)")
    pattern_result = '{result}'

    def __init__(self,
                 url: str,
                 file: str):
        self.url = url
        with open(file) as fh:
            self.conf = yaml.load(fh, Loader=yaml.FullLoader)

    async def create(self):
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


    def empty(self) -> AnswerModel:
        return AnswerModel(
            text=random.choice(self.conf.get('no_answer')),
            intent='No answer',
            metadata = {}
        )

    async def ask(self, text: str, request: Request) -> AnswerModel:
        cl = await self.search_class(text, request)
        if not cl:
            return self.empty()
        else:
            intent = cl.get('name')
            data = self.get_entity(intent)
            if not data:
                return self.empty()
            lcs = LCS(text, cl['document'])
            entity = data.get('entity')
            text.replace(lcs, '')
            item = await self.search_entity(text.replace(lcs, ''), entity, request)
            if not item:
                return self.empty()
            else:
                return AnswerModel(
                    text=self.refactor_answer(data, item),
                    intent=intent,
                    entity=entity,
                    metadata = item
                )

    def refactor_answer(self, conf, result):
        data = result[conf.get('attribute')]
        answer = conf.get('answer')
        if isinstance(data, int):
            matchValue = re.findall(self.pattern, answer)
            val = inflect_with_num(data, matchValue[0].split('|'))
            answer = answer.replace(f'({matchValue[0]})', val)
            data = number_to_words(data)

        answer = answer.replace(self.pattern_result, data)
        answer = answer.replace('{entity}', result.get('document'))
        answer = answer.replace('. ', '')
        return answer

    def get_entity(self, text: str):
        for item in self.conf.get('intents'):
            if text == item.get('name'):
                return item

    async def search(self,
                     request: Request,
                     text: str,
                     collection: str,
                     type: str = None):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Forwarded-For': request.headers.get('X-Forwarded-For'),
            'X-Request-Id': request.headers.get('X-Request-Id')
        }
        try:
            params = {'text': text}
            if type:
                params['collection_name'] = type
            response = await get_request(self.url.replace(pars, collection), head=headers, params=params)
            return response.get('metadata')
        except Exception:
            return None


    async def search_entity(self, text: str, type,  request: Request):
        res = await self.search(request = request,
                     text=text,
                     collection=entity,
                     type=type)
        return res

    async def search_class(self, text: str, request: Request):
        res = await self.search(request=request,
                                text=text,
                                collection=intent,
                                type=None)
        return res
