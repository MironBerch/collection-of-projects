from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from movies.models import Filmwork
from movies.repositories import FilmworkRepository

from . import openapi
from .serializers import FilmworkSerializer


class MovieViewSet(ReadOnlyModelViewSet):
    """Viewset для работы с кинопроизведениями."""

    queryset = Filmwork.objects.none()
    permission_classes = (AllowAny, )
    serializer_class = FilmworkSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = (
        'title',
        'access_type',
        'release_date',
        'rating',
        'type',
        'age_rating',
    )
    search_fields = (
        'title',
        'genres',
        'actors',
        'directors',
        'writers',
    )

    def get_queryset(self):
        return FilmworkRepository.get_filmworks_with_related_data()

    @openapi.filmwork_list
    def list(self, request, *args, **kwargs):
        return super(MovieViewSet, self).list(request, *args, **kwargs)

    @openapi.filmwork_detail
    def retrieve(self, request, *args, **kwargs):
        return super(MovieViewSet, self).retrieve(request, *args, **kwargs)
