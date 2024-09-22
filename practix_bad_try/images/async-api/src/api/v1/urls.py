from fastapi import APIRouter

from src.api.v1.handlers import health

api_v1_router = APIRouter(prefix='/v1')

# Healthcheck
api_v1_router.include_router(router=health.router, prefix='/healthcheck')
