from django.urls import path

from search.views import SearchAPIView


urlpatterns = [
    path(
        route='',
        view=SearchAPIView.as_view(),
        name='search',
    ),
]
