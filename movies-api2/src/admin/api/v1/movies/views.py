from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

from api.pagination import ResultsSetPagination
from api.views import MultiSerializerViewSetMixin
from movies.models import Filmwork
from movies.repositories import FilmworkRepository

from api.v1.movies.openapi import filmwork_detail, filmwork_list
from api.v1.movies.serializers import FilmworkSerializer


class MovieViewSet(
    MultiSerializerViewSetMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    """Viewset for working with films."""

    queryset = Filmwork.objects.none()
    permission_classes = (AllowAny, )
    pagination_class = ResultsSetPagination
    serializer_classes = {
        'list': FilmworkSerializer,
        'retrieve': FilmworkSerializer,
    }

    def get_queryset(self):
        return FilmworkRepository.get_filmworks_with_related_data()

    @filmwork_list
    def list(self, request, *args, **kwargs):
        return super(MovieViewSet, self).list(request, *args, **kwargs)

    @filmwork_detail
    def retrieve(self, request, *args, **kwargs):
        return super(MovieViewSet, self).retrieve(request, *args, **kwargs)
