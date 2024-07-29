from contextlib import asynccontextmanager

from api import setup_routers
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from authlib.integrations.httpx_client import AsyncOAuth2Client
from core import config, oauth2
from db import postgres, redis
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, ORJSONResponse
from fastapi_pagination import add_pagination
from middleware.main import setup_middleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from utils.jaeger import configure_tracer

settings = config.APPSettings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.jaeger.enable:
        configure_tracer(
            host=settings.jaeger.host,
            port=settings.jaeger.port,
            service_name=settings.project_name)

    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port)
    postgres.async_engine = create_async_engine(
        settings.db_dsn,
        pool_pre_ping=True, pool_size=20, pool_timeout=30)
    postgres.async_session_factory = sessionmaker(
        postgres.async_engine,
        expire_on_commit=False,
        autoflush=True,
        class_=AsyncSession)
    oauth2.google_client = AsyncOAuth2Client(
        client_id=settings.auth.google_client_id,
        client_secret=settings.auth.google_client_secret,
        redirect_uri=settings.auth.google_redirect_url,
        scope='openid email profile')
    yield
    await postgres.async_engine.dispose()
    postgres.async_session_factory.close_all()
    await redis.redis.close()
    await oauth2.google_client.aclose()


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
