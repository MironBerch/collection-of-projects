from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('yatube.urls')),
]


handler403 = 'yatube.views.permission_denied'
handler404 = 'yatube.views.page_not_found'
handler500 = 'yatube.views.server_error'


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )