from logging import config as logging_config
import os

from pydantic import Field
from pydantic_settings import BaseSettings

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


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


bucket_settings = BucketSettings()
