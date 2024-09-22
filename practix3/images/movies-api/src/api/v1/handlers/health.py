from fastapi import APIRouter

router = APIRouter(tags=['health'])


@router.get('/health', summary='Service health')
async def healthcheck() -> dict[str, str]:
    """Проверка работоспособности сервиса."""
    return {'status': 'ok'}
