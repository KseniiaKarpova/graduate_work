from contextlib import asynccontextmanager

from middleware import CheckRequest
from api.v1 import entity, intent
from core.config import settings
from db import qdrant, redis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from services import translator


@asynccontextmanager
async def lifespan(app: FastAPI):
    qdrant.client = qdrant.connect(settings.db.host, settings.db.port, settings.db.embed)
    translator.model = translator.load_model()
    translator.tokenizer = translator.init_tokenizer()
    translator.translation_pipeline = translator.init_translator()
    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port)
    yield
    await redis.redis.close()
    await qdrant.client.close()


app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


app.add_middleware(CheckRequest)
app.include_router(intent.router, prefix='/api/v1/intent', tags=['intent'])
app.include_router(entity.router, prefix='/api/v1/entity', tags=['entity'])
