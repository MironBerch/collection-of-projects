from django import template


register = template.Library()


@register.filter
def index(indexable, i):
    """Add index"""
    return indexable[i]
