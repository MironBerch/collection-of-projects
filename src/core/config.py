from os import environ

from pydantic import Field
from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    host: str = environ.get('POSTGRES_HOST')
    port: int = int(environ.get('POSTGRES_PORT'))
    db: str = environ.get('POSTGRES_NAME')
    user: str = environ.get('POSTGRES_USER')
    password: str = environ.get('POSTGRES_PASSWORD')


class FastapiConfig(BaseSettings):
    host: str = '0.0.0.0'
    port: int = 8000


class Settings(BaseSettings):
    fastapi: FastapiConfig = Field(default_factory=FastapiConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)


settings = Settings()
