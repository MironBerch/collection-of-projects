from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from search.pagination import SearchPagination
from accounts.serializers import UserSerializer
from search.services import get_search_queryset


class SearchAPIView(ListAPIView):
    filter_backends = [SearchFilter]
    pagination_class = SearchPagination
    permission_classes = (IsAuthenticated,)
    search_fields = (
        'username',
        'first_name',
        'last_name',
    )
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_search_queryset()
