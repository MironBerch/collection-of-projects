from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import MovieViewSet

app_name = 'movies'

router = SimpleRouter(trailing_slash=False)
router.register('', MovieViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
