from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import MongoDsn

load_dotenv()


class MongoSettings(BaseSettings):
    uri: MongoDsn = ...
    db_name: str = ...
    model_config: str = SettingsConfigDict(env_prefix='history_mongodb_')


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
    project_name: str = 'Auth API'
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()
    hasher: HasherSettings = HasherSettings()
    jaeger: JaegerSettings = JaegerSettings()
    file_service: FileAPISettings = FileAPISettings()


settings = APPSettings()
