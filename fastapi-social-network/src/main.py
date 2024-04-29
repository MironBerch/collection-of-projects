import logging

import uvicorn

from fastapi import FastAPI

from api.urls import api_router


app = FastAPI(
    title='Social Network API v1',
    version='1.0',
)


@app.on_event('startup')
async def startup():
    pass
    #database.connection = database.create_connection()


@app.on_event('shutdown')
async def shutdown():
    pass
    #database.connection.close()


app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8080,
        log_level=logging.DEBUG,
        reload=True,
    )
