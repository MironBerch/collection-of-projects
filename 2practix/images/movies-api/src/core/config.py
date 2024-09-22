from os import environ

DEBUG = environ.get('MOVIES_API_DEBUG') == 'True'

REDIS_HOST = 'redis'
REDIS_PORT = 6379

ELASTIC_HOST = 'elastic'
ELASTIC_PORT = 9200

FASTAPI_HOST = '0.0.0.0'
FASTAPI_PORT = 8080
