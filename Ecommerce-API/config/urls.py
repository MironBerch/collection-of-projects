from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from dj_rest_auth.registration.views import (
    VerifyEmailView,
    ResendEmailVerificationView,
)
from dj_rest_auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
    LogoutView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(
        route='resend-email/',
        view=ResendEmailVerificationView.as_view(),
        name="rest_resend_email"
    ),
    re_path(
        route=r'^account-confirm-email/(?P<key>[-:\w]+)/$',
        view=VerifyEmailView.as_view(),
        name='account_confirm_email',
    ),
    path(
        route='account-email-verification-sent/',
        view=TemplateView.as_view(),
        name='account_email_verification_sent',
    ),

    path(
        route='password/reset/',
        view=PasswordResetView.as_view(),
        name='rest_password_reset'
    ),
    path(
        route='password/reset/confirm/<str:uidb64>/<str:token>',
        view=PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    path(
        route='password/change/',
        view=PasswordChangeView.as_view(),
        name='rest_password_change'
    ),

    path(
        route='logout/',
        view=LogoutView.as_view(),
        name='rest_logout'
    ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)

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
