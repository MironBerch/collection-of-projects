from drf_spectacular.utils import extend_schema

from .serializers import FilmworkSerializer

filmwork_list = extend_schema(
    summary='Список фильмов.',
    description='Получите список фильмов.',
    responses={
        '200': FilmworkSerializer,
        '201': None,
        '400': None,
        '401': None,
    },
)

filmwork_detail = extend_schema(
    summary='Фильм.',
    description='Получите подробную информацию о фильме по `id`.',
    responses={
        '200': FilmworkSerializer,
        '201': None,
        '400': None,
        '401': None,
    },
)
