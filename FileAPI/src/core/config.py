import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class RedisSettings(BaseSettings):
    host: str = ...
    port: int = ...

    model_config = SettingsConfigDict(env_prefix='redis_')


class AuthSettings(BaseSettings):
    secret_key: str = ...
    jwt_algorithm: str = ...
    google_client_id: str = ...
    google_client_secret: str = ...
    google_token_url: str = ...
    google_base_url: str = ...
    google_userinfo_url: str = ...
    google_redirect_url: str = ...
    model_config: str = SettingsConfigDict(env_prefix='auth_')


class HasherSettings(BaseSettings):
    algorithm: str = ...
    rounds: int = ...
    model_config: str = SettingsConfigDict(env_prefix='hasher_')


class BucketSettings(BaseSettings):
    bucket_movies: str = os.getenv('BUCKET_MOVIES', 'movies')
    movies_path: str = Field('movie/')


class Settings(BaseSettings):
    project_name: str = Field('File API', env='PROJECT_NAME')

    minio_host: str = Field('minio', env='S3_HOST')
    minio_port: int = Field(9000, env='S3_PORT')
    minio_user: str = Field('adminS3', env='S3_USER')
    minio_password: str = Field('adminS3pass', env='S3_PASSWORD')

    observer_host: str = Field('postgres_file_api', env='OBSERVER_PG_HOST')
    observer_port: int = Field('5432', env='OBSERVER_PG_PORT')
    observer_user: str = Field('user', env='OBSERVER_PG_USER')
    observer_password: str = Field('user123', env='OBSERVER_PG_PASSWORD')
    observer_database: str = Field('file_api', env='OBSERVER_PG_NAME')
    observer_type: str = Field('postgresql+asyncpg', env='OBS_TYPE')
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()
    hasher: HasherSettings = HasherSettings()


bucket_settings = BucketSettings()
settings = Settings()
