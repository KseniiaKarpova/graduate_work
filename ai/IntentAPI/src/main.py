from contextlib import asynccontextmanager

from api.v1 import bot
from core.config import settings
from middleware import CheckRequest
from db import redis
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from services import facade


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port)
    facade.facade = facade.Facade(settings.t2v.url, settings.conf)
    await facade.facade.create()
    yield
    await redis.redis.close()


app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


app.add_middleware(CheckRequest)
app.include_router(bot.router, prefix='/api/v1', tags=['bot'])
