import logging
from contextlib import asynccontextmanager
from db import redis
import uvicorn
from core.config import settings
from core.logger import LOGGING
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from utils.constraint import RequestLimit
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







if __name__ == '__main__':
    uvicorn.run(
        app,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
