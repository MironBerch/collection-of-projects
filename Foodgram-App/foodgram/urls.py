from django.urls import path, include
from foodgram.views import SignUp, index, user_page, feed, recipe_page, new_recipe, edit_recipe, favorites, wishlist, download_wishlist, add_to_favorite, remove_recipe, add_wishlist, follow, remove_recipe
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path('auth/signup/', SignUp.as_view(), name='signup'),

    path('', index, name='index'),
    path('feed', feed, name='feed'),
    path('new', new_recipe, name='new'),
    path('favorites', favorites, name='favorites'),
    path('add_to_favorite/<int:recipe_id>', add_to_favorite, name='add_to_favorite'),
    path('wishlist', wishlist, name='wishlist'),
    path('<str:username>/<int:recipe_id>/remove_recipe', remove_recipe, name='remove_recipe'),
    path('wishlist/download', download_wishlist, name='download_wishlist'),
    path('<str:username>', user_page, name='user'),
    path('<str:username>/follow', follow, name='follow'),
    path('<str:username>/<int:recipe_id>', recipe_page, name='recipe'),
    path('<str:username>/<int:recipe_id>/add_wishlist', add_wishlist, name='add_wishlist'),
    path('<str:username>/<int:recipe_id>/edit', edit_recipe, name='edit_recipe'),
]