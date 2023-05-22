from django.urls import path

from accounts.views import SignupAPIView, SigninAPIView


urlpatterns = [
    path(
        route='signup/',
        view=SignupAPIView.as_view(),
        name='signup',
    ),
    path(
        route='signin/',
        view=SigninAPIView.as_view(),
        name='signin',
    ),
]
