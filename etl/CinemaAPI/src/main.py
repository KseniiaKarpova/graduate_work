import logging
from contextlib import asynccontextmanager

import uvicorn
from api.v1 import films, genres, persons
from core import config
from core.logger import LOGGING
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from middleware import CheckRequest, RateLimitMiddleware, JWTMiddleware
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis
from utils.constraint import RequestLimit
from utils.jaeger import configure_tracer

settings = config.Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.jaeger_enable:
        configure_tracer(
            host=settings.jaeger_host,
            port=settings.jaeger_port,
            service_name=settings.project_name)

    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    elastic.es = AsyncElasticsearch(
        hosts=[f'http://{settings.es_host}:{settings.es_port}'])
    yield
    await redis.redis.close()
    await elastic.es.close()


app = FastAPI(
    title=settings.project_name,
    description="Information about films, genres and actors",
    docs_url='/cinema/openapi',
    openapi_url='/cinema/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


FastAPIInstrumentor.instrument_app(app)
app.add_middleware(CheckRequest)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(JWTMiddleware)
app.include_router(films.router, prefix='/cinema/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/cinema/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/cinema/api/v1/persons', tags=['persons'])


if __name__ == '__main__':
    uvicorn.run(
        app,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
