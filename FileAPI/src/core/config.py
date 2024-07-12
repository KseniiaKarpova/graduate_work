import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class BucketSettings(BaseSettings):
    bucket_movies: str = os.getenv('BUCKET_MOVIES', 'movies')
    movies_path: str = Field('movie/')


class MinioSettings(BaseSettings):
    host: str = ...
    port: int = ...
    user: str = ...
    password: str = ...
    model_config: str = SettingsConfigDict(env_prefix='s3_')

    @property
    def endpoint(self):
        return f'{self.host}:{self.port}'


class Settings(BaseSettings):
    project_name: str = os.getenv('PROJECT_NAME', 'File API')

    minio: MinioSettings = MinioSettings()
    observer_host: str = os.getenv('FILE_POSTGRES_HOST')
    observer_port: int = os.getenv('FILE_POSTGRES_PORT')
    observer_user: str = os.getenv('FILE_POSTGRES_USER')
    observer_password: str = os.getenv('FILE_POSTGRES_PASSWORD')
    observer_database: str = os.getenv('FILE_POSTGRES_NAME')
    observer_type: str = os.getenv('OBS_TYPE')


bucket_settings = BucketSettings()
