from yatube.views import *
from django.urls import path
from django.contrib.auth.views import *


urlpatterns = [
    path('auth/signup/', SignUp.as_view(), name='signup'),
    path('auth/logout/',LogoutView.as_view(template_name='users/logged_out.html'),name='logout'),
    path('auth/login/',LoginView.as_view(template_name='users/login.html'),name='login'),
    path('auth/password_change/',PasswordChangeView.as_view(template_name='users/password_change_form.html'),name='password_change'),
    path('auth/password_change/done/',PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),name='password_change_done'),
    path('auth/password_reset/',PasswordResetView.as_view(template_name='users/password_reset_form.html'),name='password_reset'),
    path('auth/password_reset/done/',PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('auth/reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('auth/reset/done/',PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),

    path('', index, name='index'),
    path('group/<slug:slug>/', group_posts, name='group_list'),
    path('profile/<str:username>/', profile, name='profile'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('create/', post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('posts/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('follow/', follow_index, name='follow_index'),
    path('profile/<str:username>/follow/', profile_follow, name='profile_follow'),
    path('profile/<str:username>/unfollow/', profile_unfollow, name='profile_unfollow'),
]