from fastapi import APIRouter

from models.health import HealthCheckResponse

router = APIRouter(tags=['health'])


@router.get(
    '/health',
    summary='Service health',
    response_model=HealthCheckResponse,
    responses={
        200: {
            'description': 'Success',
            'content': {
                'application/json': {
                    'example': {'status': 'ok'}
                },
            },
        },
    },
)
async def healthcheck():
    """Проверка работоспособности сервиса."""
    return {'status': 'ok'}
