import logging
from contextlib import asynccontextmanager

import uvicorn
from api import setup_routers
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from core import config, logger
from core.logger import setup_root_logger
from db import init_db, mongo, redis
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, ORJSONResponse
from fastapi_pagination import add_pagination
from middleware.main import setup_middleware
from motor.motor_asyncio import AsyncIOMotorClient
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis
from utils.constraint import RequestLimit
from utils.jaeger import configure_tracer

settings = config.APPSettings()

setup_root_logger()


@asynccontextmanager
async def lifespan(_: FastAPI):
    mongo.mongo_client = AsyncIOMotorClient(str(settings.mongodb.uri), uuidRepresentation='standard')
    await init_db.init(client=mongo.mongo_client)
    if settings.jaeger.enable:
        configure_tracer(
            host=settings.jaeger.host,
            port=settings.jaeger.port,
            service_name=settings.project_name)
    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port)
    yield
    await redis.redis.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        description="Auth logic",
        docs_url='/api/openapi',
        openapi_url='/api/openapi.json',
        default_response_class=ORJSONResponse,
        lifespan=lifespan
    )
    setup_middleware(app)
    setup_routers(app)
    add_pagination(app)
    return app


app = create_app()


FastAPIInstrumentor.instrument_app(app)



@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code, content={
            "detail": exc.message})
