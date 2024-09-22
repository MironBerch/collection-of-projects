from os import environ

POSTGRES_DB: str = environ.get('POSTGRES_DB')
POSTGRES_USER: str = environ.get('POSTGRES_USER')
POSTGRES_PASSWORD: str = environ.get('POSTGRES_PASSWORD')
