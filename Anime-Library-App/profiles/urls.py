from django.urls import path

from profiles.views import ProfileEdit, ProfileView


urlpatterns = [
    path(
        route='account/<str:username>/',
        view=ProfileEdit.as_view(),
        name='profile_edit',
    ),
    path(
        route='<str:username>/',
        view=ProfileView.as_view(),
        name='profile_view',
    ),
]