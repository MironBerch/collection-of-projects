from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import (
    AddressViewSet,
    ProfileAPIView,
    SendOrResendSMSAPIView,
    UserAPIView,
    UserLoginAPIView,
    UserRegisterationAPIView,
    VerifyPhoneNumberAPIView,
)


router = DefaultRouter()
router.register(r'', AddressViewSet)

urlpatterns = [
    path(
        route='register/',
        view=UserRegisterationAPIView.as_view(),
        name='user_register'
    ),
    path(
        route='login/',
        view=UserLoginAPIView.as_view(),
        name='user_login',
    ),

    path(
        route='send-sms/',
        view=SendOrResendSMSAPIView.as_view(),
        name='send_resend_sms'
    ),
    path(
        route='verify-phone/',
        view=VerifyPhoneNumberAPIView.as_view(),
        name='verify_phone_number'
    ),

    path(
        route='',
        view=UserAPIView.as_view(),
        name='user_detail'
    ),
    path(
        route='profile/',
        view=ProfileAPIView.as_view(),
        name='profile_detail'
    ),

    path('profile/address/', include(router.urls)),
]
