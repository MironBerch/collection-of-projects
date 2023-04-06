from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from authy.views import UserProfile, UserProfileFavorites, follow


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('authy.urls')),
    path('post/', include('post.urls')),
    path('direct/', include('direct.urls')),
    path('notifications/', include('notifications.urls')),
    path('<username>/', UserProfile, name='profile'),
    path('<username>/saved', UserProfile, name='profilefavorites'),
    path('<username>/follow/<option>', follow, name='follow'),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
