from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from ecommerce.views import signup


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', signup, name='signup'),
    path('accounts/login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='account/logout.html'), {'next_page' : 'login'}, name='logout'),
    path('', include('ecommerce.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)