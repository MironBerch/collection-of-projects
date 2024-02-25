from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from movies.api.pagination import ResultsSetPagination
from movies.api.views import MultiSerializerViewSetMixin
from movies.models import Filmwork
from movies.repositories import FilmworkRepository

from . import openapi
from .serializers import FilmworkSerializer


class MovieViewSet(
    MultiSerializerViewSetMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    """Viewset для работы с фильмами."""

    queryset = Filmwork.objects.none()
    permission_classes = (AllowAny, )
    serializer_classes = {
        'list': FilmworkSerializer,
        'retrieve': FilmworkSerializer,
    }
    pagination_class = ResultsSetPagination
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
