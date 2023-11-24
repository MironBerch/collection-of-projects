from os import environ

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: int = int(environ.get(key='DEBUG', default=1))
    project_full_domain: str = environ.get('PROJECT_FULL_DOMAIN')
    project_domain: str = environ.get('PROJECT_DOMAIN')

    postgres_db: str = environ.get('POSTGRES_DB')
    postgres_user: str = environ.get('POSTGRES_USER')
    postgres_password: str = environ.get('POSTGRES_PASSWORD')
    postgres_host: str = environ.get('POSTGRES_HOST')
    postgres_port: int = environ.get('POSTGRES_PORT')

    postgres_url: str = f'{postgres_user}:{postgres_password}@{postgres_host}:\
        {postgres_port}/{postgres_db}'

    celery_broker_url: str = environ.get('CELERY_BROKER_URL')

    cookie_max_age: int = 3600

    access_token_expire_seconds: int = 3600
    jwt_secret_key: str = environ.get('JWT_SECRET_KEY')

    email_host_user: str = environ.get('EMAIL_HOST_USER')
    email_host: str = 'smtp.gmail.com'
    email_port: int = 465
    email_host_password: str = environ.get('EMAIL_HOST_PASSWORD')


settings = Settings()
