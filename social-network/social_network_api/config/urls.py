from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/search/', include('search.urls')),
    path('api/notifications/', include('notifications.urls')),
]

urlpatterns += [
    path(
        route='api/schema/',
        view=SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        route='',
        view=SpectacularSwaggerView.as_view(
            url_name='schema'
        ),
        name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
