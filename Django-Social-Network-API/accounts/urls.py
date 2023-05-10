from django.urls import path
from knox.views import LogoutView, LogoutAllView

from accounts.views import SignupView, SigninView


urlpatterns = [
    path(
        'signup/',
        SignupView.as_view(),
        name='signup',
    ),
    path(
        'signin/',
        SigninView.as_view(),
        name='signin',
    ),
    path(
        'signout/',
        LogoutView.as_view(),
        name='signout',
    ),
    path(
        'signoutall/',
        LogoutAllView.as_view(),
        name='signoutall',
    ),
]
