import logging

from core import config
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from middleware.request_log import RequestLogMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from middleware import CheckRequest

settings = config.APPSettings()


logger = logging.getLogger(__name__)


def setup_middleware(app: FastAPI):
    app.add_middleware(SessionMiddleware, secret_key=settings.auth.secret_key)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex='.*',
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.add_middleware(RequestLogMiddleware)
    app.add_middleware(CheckRequest)
