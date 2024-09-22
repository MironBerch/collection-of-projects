import logging

import uvicorn
from elasticsearch import AsyncElasticsearch
from redis import Redis

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.urls import api_router
from core.config import settings
from db import elastic, redis

app = FastAPI(
    title='Movies API v1',
    description='Read-only movies API',
    version='1.0',
    docs_url='/movie/api/v1/docs',
    openapi_url='/movie/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True,
    )
    elastic.elastic = AsyncElasticsearch(
        hosts=[
            f'http://{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}',
        ],
    )


@app.on_event('shutdown')
async def shutdown():
    redis.redis.connection_pool.disconnect()
    await elastic.elastic.close()


app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host=settings.FASTAPI_HOST,
        port=settings.FASTAPI_PORT,
        log_level=logging.DEBUG,
        reload=True,
    )
