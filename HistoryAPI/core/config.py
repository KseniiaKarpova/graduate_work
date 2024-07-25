from dotenv import load_dotenv
from pydantic import MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class MongoSettings(BaseSettings):
    uri: MongoDsn = ...
    db_name: str = ...
    model_config: str = SettingsConfigDict(env_prefix='history_mongo_')


class RedisSettings(BaseSettings):
    host: str = ...
    port: int = ...

    model_config = SettingsConfigDict(env_prefix='redis_')


class AuthSettings(BaseSettings):
    secret_key: str = ...
    jwt_algorithm: str = ...
    model_config: str = SettingsConfigDict(env_prefix='auth_')


class LoggerSettings(BaseSettings):
    filename: str = ...
    maxbytes: int = ...
    mod: str = ...
    backup_count: str = ...
    log_level: str = ...
    sentry_dsn: str = ...
    model_config: str = SettingsConfigDict(env_prefix='history_logger_')


class FileAPISettings(BaseSettings):
    host: str = ...
    port: int = ...
    url: str = ...
    model_config: str = SettingsConfigDict(env_prefix='file_api_')

    @property
    def path(self) -> str:
        return f"http://{self.host}:{self.port}{self.url}"


class HasherSettings(BaseSettings):
    algorithm: str = ...
    rounds: int = ...
    model_config: str = SettingsConfigDict(env_prefix='hasher_')


class JaegerSettings(BaseSettings):
    host: str = ...
    port: int = ...
    enable: bool = ...
    model_config: str = SettingsConfigDict(env_prefix='jaeger_')


class APPSettings(BaseSettings):
    project_name: str = 'History API'
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()
    hasher: HasherSettings = HasherSettings()
    jaeger: JaegerSettings = JaegerSettings()
    file_service: FileAPISettings = FileAPISettings()
    mongodb: MongoSettings = MongoSettings()
    logger: LoggerSettings = LoggerSettings()


settings = APPSettings()
