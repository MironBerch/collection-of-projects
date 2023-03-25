from atexit import register
from django import template
from foodgram.models import Wishlist


register = template.Library()


@register.filter
def wishlist_count(user):
    """Calculates the number of recipes in the shopping list"""
    return Wishlist.objects.filter(user_id=user.id).count()