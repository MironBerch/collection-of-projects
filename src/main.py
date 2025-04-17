from logging import DEBUG

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.urls import api_router

app = FastAPI(
    title='Capybara API',
    docs_url='/api/docs',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        log_level=DEBUG,
        reload=True,
    )
