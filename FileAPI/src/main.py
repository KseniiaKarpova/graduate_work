from contextlib import asynccontextmanager

from api.v1 import file
from core import config
from db import minio, postgres, redis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from miniopy_async import Minio
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

settings = config.Settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    minio.minio = Minio(
        endpoint=f'{settings.minio_host}:{settings.minio_port}',
        access_key=settings.minio_user,
        secret_key=settings.minio_password,
        secure=False,
    )
    result = await minio.minio.bucket_exists(config.bucket_settings.bucket_movies)
    if not result:
        await minio.minio.make_bucket(config.bucket_settings.bucket_movies)

    postgres.engine = create_async_engine(
        settings.postgres_path,
        echo=True,
    )
    postgres.async_session = async_sessionmaker(postgres.engine, class_=AsyncSession, expire_on_commit=False)
    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port)
    yield
    await postgres.engine.dispose()
    await redis.redis.close()


app = FastAPI(
    title=settings.project_name,
    description="Upload and download files",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


app.include_router(file.router, prefix='/api/v1', tags=['file'])
