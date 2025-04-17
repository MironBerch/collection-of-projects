from pydantic import BaseModel

from fastapi import APIRouter, status

router = APIRouter(tags=['healthcheck'])


class HealthCheck(BaseModel):
    status: str


@router.get(
    '/healthcheck',
    summary='Health check',
    response_model=HealthCheck,
    responses={
        200: {
            'description': 'Success',
            'content': {
                'application/json': {
                    'example': {'status': 'ok'},
                },
            },
        },
    },
    status_code=status.HTTP_200_OK,
)
async def healthcheck() -> HealthCheck:
    return {'status': 'ok'}
