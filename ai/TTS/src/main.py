from contextlib import asynccontextmanager

from api.v1 import tts
from core.config import settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from model.v2 import manager


@asynccontextmanager
async def lifespan(_: FastAPI):
    manager.init(settings.tts.name)
    yield


def create_app() -> FastAPI:
    application = FastAPI(
        lifespan=lifespan,
        title='TTS',
        docs_url='/api/openapi',
        openapi_url='/api/openapi.json',
        default_response_class=ORJSONResponse,
        description='Text to Speach',
        version='0.1.0',
    )
    return application


app = create_app()

app.include_router(tts.router, prefix='/api/v1', tags=['tts'])
