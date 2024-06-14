from fastapi import FastAPI

from api.routers import router
import uvicorn

app = FastAPI(
    title='Movies API v1',
    docs_url='/api/docs',
    openapi_url='/api/openapi.json',
)

app.include_router(router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
