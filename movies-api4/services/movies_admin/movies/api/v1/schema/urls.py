from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from django.urls import path

urlpatterns = [
    path(
        route='',
        view=SpectacularAPIView.as_view(),
        name='schema',
    ),
    path(
        route='redoc/',
        view=SpectacularRedocView.as_view(url_name='v1:schema'),
        name='redoc',
    ),
    path(
        route='swagger/',
        view=SpectacularSwaggerView.as_view(url_name='v1:schema'),
        name='swagger',
    ),
]
