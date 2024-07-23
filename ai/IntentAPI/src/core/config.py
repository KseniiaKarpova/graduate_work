from fastapi import Query
from pydantic_settings import BaseSettings, SettingsConfigDict


class QueryParams:
    def __init__(
        self,
        page_number: int | None = Query(default=1, ge=1),
        page_size: int | None = Query(default=10, ge=1, le=50),
    ):
        self.page_number = page_number
        self.page_size = page_size


class AuthSettings(BaseSettings):
    secret_key: str = ...
    jwt_algorithm: str = ...
    model_config: str = SettingsConfigDict(env_prefix='auth_')


class RedisSettings(BaseSettings):
    host: str = ...
    port: str = ...
    model_config: str = SettingsConfigDict(env_prefix='redis_intent_')


class Text2VecSettings(BaseSettings):
    host: str = ...
    port: int = ...
    model_config: str = SettingsConfigDict(env_prefix='t2v_')

    @property
    def url(self):
        return f"http://{self.host}:{self.port}/api/v1/[type]/"


class CinemaSettings(BaseSettings):
    host: str = ...
    port: int = ...
    model_config: str = SettingsConfigDict(env_prefix='cinema_')

    @property
    def url(self):
        return f"http://{self.host}:{self.port}"

class APPSettings(BaseSettings):
    project_name: str = 'Intent API'
    conf: str = 'conf.yaml'
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()
    t2v: Text2VecSettings = Text2VecSettings()
    cinema = CinemaSettings()


settings = APPSettings()
