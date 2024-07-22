import requests
import os
from dotenv import load_dotenv
import time


load_dotenv()

HOST = os.environ.get('t2v_host')
PORT = os.environ.get('t2v_port')
URL = f"http://{HOST}:{PORT}/api/v1/entity/"


def insert_to_entity(index: str, text: str, metadata: dict = {}):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Forwarded-For': metadata.get('id', 'ETL'),
        'X-Request-Id': metadata.get('id', 'elt')
    }
    json_data = {
        'collection_name': index,
        'id': None,
        'text': text,
        'metadata': metadata,
    }
    response = requests.post(URL, headers=headers, json=json_data)
    print(response.text)
    time.sleep(1)