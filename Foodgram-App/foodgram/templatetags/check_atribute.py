from atexit import register
from django import template
from foodgram.models import Wishlist, Favorites, Follow


register = template.Library()


@register.filter
def check_wishlist(recipe, user):
    """Сhecks is recipe add in wish list"""
    check = Wishlist.objects.filter(
        recipe_id=recipe.id, user_id=user.id
    ).exists()
    
    return check


@register.filter
def check_favorite(recipe, user):
    """Check is recipe add in favorite"""
    check = Favorites.objects.filter(
        recipe_id=recipe.id, user_id=user.id
    ).exists()

    return check


@register.filter
def check_subscription(author, user):
    """Check is user subscription on author"""
    check = Follow.objects.filter(
        following=author.id, subscriber=user.id
    ).exists()
    
    return check