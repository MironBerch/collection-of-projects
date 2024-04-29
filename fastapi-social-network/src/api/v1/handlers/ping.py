from fastapi import APIRouter

router = APIRouter(tags=['ping'])


@router.get('/ping')
async def healthcheck():
    """Проверка работоспособности сервиса."""
    return {'status': 'ok'}
