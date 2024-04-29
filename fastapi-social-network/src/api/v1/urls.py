from fastapi import APIRouter

from api.v1.handlers import ping, countries

api_v1_router = APIRouter(prefix='')

# Healthcheck
api_v1_router.include_router(router=ping.router, prefix='')
api_v1_router.include_router(router=countries.router, prefix='')
