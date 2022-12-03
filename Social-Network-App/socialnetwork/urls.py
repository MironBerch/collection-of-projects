from django.urls import path
from socialnetwork.views import index, settings, upload, follow, search, profile, like_post, signup, signin, logout


urlpatterns = [
    path('', index, name='index'),
    path('settings', settings, name='settings'),
    path('upload', upload, name='upload'),
    path('follow', follow, name='follow'),
    path('search', search, name='search'),
    path('profile/<str:pk>', profile, name='profile'),
    path('like-post', like_post, name='like-post'),
    path('signup', signup, name='signup'),
    path('signin', signin, name='signin'),
    path('logout', logout, name='logout'),
]