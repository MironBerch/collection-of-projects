from os import environ

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str = environ.get('REDIS_HOST')
    redis_port: int = environ.get('REDIS_PORT')
    redis_db: int = environ.get('REDIS_DB')

    elastic_host: str = environ.get('ELASTIC_HOST')
    elastic_port: int = environ.get('ELASTIC_PORT')

    fastapi_host: str = '0.0.0.0'
    fastapi_port: int = environ.get('FASTAPI_PORT')


settings = Settings()
