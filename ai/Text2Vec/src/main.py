import logging
from contextlib import asynccontextmanager

import uvicorn
from api.v1 import entity, intent
from core.config import settings
from core.logger import LOGGING
from db import qdrant, redis
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from services import translator
from utils.constraint import RequestLimit


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


@app.middleware('http')
async def before_request(request: Request, call_next):
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


app.include_router(intent.router, prefix='/api/v1/intent', tags=['intent'])
app.include_router(entity.router, prefix='/api/v1/entity', tags=['entity'])


if __name__ == '__main__':
    uvicorn.run(
        app,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
