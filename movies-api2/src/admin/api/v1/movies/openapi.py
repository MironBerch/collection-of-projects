from drf_spectacular.utils import extend_schema

from ..movies.serializers import FilmworkSerializer


filmwork_list = extend_schema(
    summary='Film list.',
    description='Get list of all films.',
    responses={
        '200': FilmworkSerializer,
        '201': None,
        '400': None,
        '401': None,
    },
)

filmwork_detail = extend_schema(
    summary='Film.',
    description='Get film details by `id`.',
    responses={
        '200': FilmworkSerializer,
        '201': None,
        '400': None,
        '401': None,
    },
)
