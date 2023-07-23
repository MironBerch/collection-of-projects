from os import environ
from typing import Optional
from datetime import timedelta

from pydantic import BaseSettings

from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    debug: bool = False

    postgres_url: str = environ.get('POSTGRES_URL')
    postgres_min_pool_size: int = environ.get('POSTGRES_MIX_POOL_SIZE')
    postgres_max_pool_size: int = environ.get('POSTGRES_MAX_POOL_SIZE')

    redis_url: str = environ.get('REDIS_URL')  # 'redis://127.0.0.1:6379'
    pubsub_url: str = environ.get('PUBSUB_URL')  # 'redis://127.0.0.1:6380'

    neo4j_url: str = environ.get('NEO4J_URL')  # 'neo4j://localhost:7687'
    neo4j_user: str = environ.get('NEO4J_USER')  # 'neo4j'
    neo4j_password: str = environ.get('NEO4J_PASSWORD')  # 'secret'

    jwt_secret: str = environ.get('JWT_SECRET')  # 'secret'
    jwt_algorithm: str = 'HS256'
    jwt_expiration_seconds: int = timedelta(minutes=15).total_seconds()
    jwt_refresh_expiration_seconds: int = timedelta(weeks=2).total_seconds()

    sentry_dsn: Optional[str] = None


settings = Settings()
print(settings)
sentry_config = dict(
    dsn=settings.sentry_dsn
)
