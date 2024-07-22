from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class PostgresDbSettings(BaseSettings):
    host: str = ...
    user: str = ...
    port: int = ...
    db: str = ...
    password: str = ...

    model_config = SettingsConfigDict(env_prefix='auth_postgres_')


class RedisSettings(BaseSettings):
    host: str = ...
    port: int = ...

    model_config = SettingsConfigDict(env_prefix='auth_redis_')


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


class JaegerSettings(BaseSettings):
    host: str = ...
    port: int = ...
    enable: bool = ...
    model_config: str = SettingsConfigDict(env_prefix='jaeger_')


class WorkerService(BaseSettings):
    host: str = ...
    port: str = ...

    model_config: str = SettingsConfigDict(env_prefix='worker_')

    @property
    def url(self):
        return f"http://{self.host}:{self.port}/api/v1"


class AdminSettings(BaseSettings):
    login: str = ...
    password: str = ...
    email: str = ...

    model_config: str = SettingsConfigDict(env_prefix='admin_')


class APPSettings(BaseSettings):
    project_name: str = 'Auth API'
    db: PostgresDbSettings = PostgresDbSettings()
    db_dsn: str = f'postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.db}'
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()
    hasher: HasherSettings = HasherSettings()
    jaeger: JaegerSettings = JaegerSettings()
    worker: WorkerService = WorkerService()
    admin: AdminSettings = AdminSettings()


settings = APPSettings()
