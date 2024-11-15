from drf_spectacular.utils import extend_schema

from .serializers import FilmworkSerializer

filmwork_list = extend_schema(
    summary='Список кинопроизведений.',
    description='Получите список кинопроизведений.',
    responses={
        '200': FilmworkSerializer,
        '201': None,
        '400': None,
        '401': None,
    },
)

filmwork_detail = extend_schema(
    summary='Кинопроизведение.',
    description='Получите подробную информацию о кинопроизведении по `id`.',
    responses={
        '200': FilmworkSerializer,
        '201': None,
        '400': None,
        '401': None,
    },
)
