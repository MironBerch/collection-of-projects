from django.urls import path

from accounts.views import SignupView, SigninView, SignoutView, EmailConfirmationView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path(
        route='signup/',
        view=SignupView.as_view(),
        name='signup',
    ),
    path(
        route='signin/',
        view=SigninView.as_view(),
        name='signin',
    ),
    path(
        route='signout/',
        view=SignoutView.as_view(),
        name='signout',
    ),
    path(
        route='password_reset/',
        view=PasswordResetView.as_view(),
        name='password_reset',
    ),
    path(
        route='password_reset/done/',
        view=PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        route='reset/<uidb64>/<token>/',
        view=PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        route='reset/done/',
        view=PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path(
        route='password_change/',
        view=PasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        route='password_change/done/',
        view=PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),
    path(
        route='email_confirmation/',
        view=EmailConfirmationView.as_view(),
        name='email_confirmation',
    ),
]