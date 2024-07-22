from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from core.config import settings
from model.v1 import manager
from api.v1 import tts

@asynccontextmanager
async def lifespan(_: FastAPI):
    manager.init(settings.tts)
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
    #setup_middleware(application)
    return application


app = create_app()

app.include_router(tts.router, prefix='/api/v1', tags=['tts'])



if __name__ == '__main__':
    uvicorn.run(
        app,
        reload=True,
    )
