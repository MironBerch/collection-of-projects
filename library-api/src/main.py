from logging import DEBUG

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
from core.logger import LOGGING


app = FastAPI(
    title='Library API',
    version='1.0',
    docs_url='/api/docs',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host=settings.fastapi.host,
        port=settings.fastapi.port,
        log_config=LOGGING,
        log_level=DEBUG,
        reload=True,
    )
