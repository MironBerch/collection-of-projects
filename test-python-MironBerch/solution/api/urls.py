from django.urls import path

from api.views import (
    AddFriendsAPIView,
    CountryListAPIView,
    CountryRetrieveAPIView,
    CreatePostAPIView,
    FriendsAPIView,
    PingView,
    ProfileAPIView,
    ProfileEditAPIView,
    RegisterAPIView,
    RemoveFriendsAPIView,
    SigninAPIView,
    UpdatePasswordAPIView,
    DetailPostAPIView,
)

urlpatterns = [
    path('ping', PingView.as_view()),
    path('countries', CountryListAPIView.as_view()),
    path('countries/<str:alpha2>', CountryRetrieveAPIView.as_view()),
    path('auth/register', RegisterAPIView.as_view()),
    path('auth/sign-in', SigninAPIView.as_view()),
    path('me/profile', ProfileEditAPIView.as_view()),
    path('profiles/<str:login>', ProfileAPIView.as_view()),
    path('me/updatePassword', UpdatePasswordAPIView.as_view()),
    path('friends/add', AddFriendsAPIView.as_view()),
    path('friends/remove', RemoveFriendsAPIView.as_view()),
    path('friends', FriendsAPIView.as_view()),
    path('posts/new', CreatePostAPIView.as_view()),
    path('posts/<str:id>', DetailPostAPIView.as_view()),
]
