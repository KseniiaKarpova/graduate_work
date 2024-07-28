import json
import time
from typing import Optional

from core.config import settings
from db.redis import get_redis
from exceptions import ForbiddenError, TokenExpiredError, UnauthorizedError, WrongDataError
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, jwt
from schemas.auth import JWTUserData


def decode_token(token: str) -> Optional[dict]:
    try:
        decoded_token = jwt.decode(
            token, settings.auth.secret_key, algorithms=[
                settings.auth.jwt_algorithm])
        if decoded_token['exp'] < time.time():
            raise ForbiddenError
        return decoded_token
    except ExpiredSignatureError:
        raise TokenExpiredError
    except Exception:
        raise WrongDataError


async def jwt_user_data(subject: dict):
    subject: dict = json.loads(subject)
    login, uuid = subject.get('login'), subject.get('uuid')
    if not login or not uuid:
        raise ForbiddenError
    return JWTUserData(login=login, uuid=uuid)


class JWTBearer(HTTPBearer):
    def __init__(
            self, auto_error: bool = True,
            token_type: str = 'access'):
        self.token_type = token_type
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        await self.check_credentials(credentials=credentials)
        decoded_token = decode_token(credentials.credentials)
        subject, jti, type = await self.check_fields(decoded_token=decoded_token)
        if type != self.token_type:
            raise ForbiddenError
        return {
            'subject': subject,
            'jti': jti,
            'type': type
        }

    async def check_denylist(self, jti):
        redis = get_redis()
        denied = await redis.get(jti)
        if denied:
            raise ForbiddenError

    async def check_credentials(self, credentials: HTTPAuthorizationCredentials):
        if not credentials:
            raise ForbiddenError
        if not credentials.scheme == 'Bearer':
            raise UnauthorizedError

    async def check_fields(self, decoded_token: dict):
        subject: dict = decoded_token.get('sub')
        jti = decoded_token.get('jti')
        type = decoded_token.get('type')
        if not subject or not jti or not type:
            raise ForbiddenError
        await self.check_denylist(jti=jti)
        return subject, jti, type


class JwtHandler:
    def __init__(self, jwt_data: dict = None) -> None:
        self.jwt_data = jwt_data

    async def get_current_user(self):
        return await jwt_user_data(subject=self.subject)

    @property
    def subject(self):
        return self.jwt_data.get('subject')


def require_access_token(
    jwt_data: dict = Depends(JWTBearer(token_type='access'))
) -> JwtHandler:
    return JwtHandler(jwt_data=jwt_data)
