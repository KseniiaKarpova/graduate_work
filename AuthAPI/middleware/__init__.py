from starlette.middleware.base import BaseHTTPMiddleware
from utils.constraint import RequestLimit
from fastapi import Request, status
from fastapi.responses import ORJSONResponse
from core import config

settings = config.APPSettings()


class CheckRequest(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user = request.headers.get('X-Forwarded-For')
        result = await RequestLimit().is_over_limit(user=user)
        if result:
            return ORJSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={
                    'detail': 'Too many requests'}
            )

        response = await call_next(request)
        request_id = request.headers.get('X-Request-Id')
        if settings.jaeger.enable is False:
            return response
        request_id = request.headers.get('request_id')
        if not request_id:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={
                    'detail': 'X-Request-Id is required'})
        return response
