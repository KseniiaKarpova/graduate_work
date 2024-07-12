import logging
from contextlib import asynccontextmanager

import uvicorn
from api.v1 import films, genres, persons
from core import config
from core.logger import LOGGING
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis
from utils.jaeger import configure_tracer
from utils.constraint import RequestLimit
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from utils.metrics import http_requested_languages_total, request_limit_exceeded

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
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)
instrumentator = Instrumentator().instrument(app,
                                             metric_namespace=settings.project_name.replace(" ", '_'),
                                             metric_subsystem=settings.project_name.replace(" ", '_')).expose(app)
instrumentator.add(http_requested_languages_total())
instrumentator.add(request_limit_exceeded())
instrumentator.add(metrics.default())
instrumentator.expose(app)


@app.middleware('http')
async def before_request(request: Request, call_next):
    if "/metrics" in str(request.url):
        response = await call_next(request)
        return response

    user = request.headers.get('X-Forwarded-For')
    result = await RequestLimit().is_over_limit(user=user)
    if result:
       return ORJSONResponse(
           status_code=status.HTTP_429_TOO_MANY_REQUESTS,
           content={'detail': 'Too many requests'}
       )

    response = await call_next(request)
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={
                'detail': 'X-Request-Id is required'})
    return response


FastAPIInstrumentor.instrument_app(app)


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])


if __name__ == '__main__':
    uvicorn.run(
        app,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
