from fastapi import Query
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class QueryParams:
    def __init__(
        self,
        page_number: int | None = Query(default=1, ge=1),
        page_size: int | None = Query(default=10, ge=1, le=50),
    ):
        self.page_number = page_number
        self.page_size = page_size


class QdrantSettings(BaseSettings):
    host: str = ...
    port: str = ...
    embed: str = ...
    threshold: float = ...
    model_config: str = SettingsConfigDict(env_prefix='qdrant_')

    @property
    def url(self):
        return f"http://{self.host}:{self.port}"


class TranslatorSettings(BaseSettings):
    checkpoint: str = ...
    source_lang: str = ...
    target_lang: str = ...
    max_length: int = ...
    model_config: str = SettingsConfigDict(env_prefix='translate_')


class AuthSettings(BaseSettings):
    secret_key: str = ...
    jwt_algorithm: str = ...
    model_config: str = SettingsConfigDict(env_prefix='auth_')


class RedisSettings(BaseSettings):
    host: str = ...
    port: str = ...
    model_config: str = SettingsConfigDict(env_prefix='REDIS_')


class APPSettings(BaseSettings):
    project_name: str = 'Text2Vec API'
    db: QdrantSettings = QdrantSettings()
    translation: TranslatorSettings = TranslatorSettings()
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()



settings = APPSettings()
