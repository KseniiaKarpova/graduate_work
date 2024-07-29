from fastapi import Request, HTTPException
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from core.handlers import JwtHandler, JWTBearer

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Call the require_access_token dependency to validate the token
            jwt_data = await JWTBearer(token_type='access')(request)
            request.state.user = await JwtHandler(jwt_data=jwt_data).get_current_user()
            response = await call_next(request)
        except HTTPException as exc:
            response = ORJSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )
        return response
