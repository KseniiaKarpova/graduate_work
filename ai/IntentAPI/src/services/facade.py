import requests
import time
import yaml
from fastapi import Request


facade = None

class Facade:

    def __init__(self,
                 url: str,
                 file: str):
        self.url = url
        with open(file) as fh:
            self.conf = yaml.load(fh, Loader=yaml.FullLoader)
        print(self.conf)

    def create(self):
        for item in self.conf.get('intents'):
            print(item)
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
            response = requests.post(self.url, headers=headers, json=json_data)
            print(response.text)
            time.sleep(5)

    def ask(self, text: str):
        pass





