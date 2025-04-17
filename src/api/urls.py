from fastapi import APIRouter

from api.handlers import health

api_router = APIRouter(prefix='/api')

# Healthcheck
api_router.include_router(router=health.router)
