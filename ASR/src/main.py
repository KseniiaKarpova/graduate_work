from api.v1 import bot
from fastapi.responses import ORJSONResponse
from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(
    title="ASR",
    description="",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(bot.router, prefix='/api/v1/audio', tags=['audio'])
