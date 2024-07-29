from starlette.middleware.base import BaseHTTPMiddleware
from utils.constraint import RequestLimit
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse, ORJSONResponse
from core.handlers import JWTBearer, JwtHandler
from core import config

settings = config.settings


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
        if settings.jaeger_enable is False:
            return response
        request_id = request.headers.get('request_id')
        if not request_id:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={
                    'detail': 'X-Request-Id is required'})
        return response


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/cinema/openapi", "/cinema/redoc", "/cinema/openapi.json"]:
            return await call_next(request)
        try:
            # Validate JWT token
            jwt_data = await JWTBearer(token_type='access')(request)
            request.state.user = await JwtHandler(jwt_data=jwt_data).get_current_user()

            response = await call_next(request)
        except HTTPException as exc:
            response = ORJSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )
        except Exception as exc:
            response = ORJSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.message},
            )
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user = request.headers.get('X-Forwarded-For')
        result = await RequestLimit().is_over_limit(user=user)
        if result:
            return ORJSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={'detail': 'Too many requests'}
            )
        response = await call_next(request)
        return response
