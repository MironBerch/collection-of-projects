from logging import DEBUG

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


app = FastAPI(
    title='Capybara API',
    docs_url='/api/docs',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        log_level=DEBUG,
        reload=True,
    )
