from django import template
from foodgram.models import TAG_CHOICES


register = template.Library()


@register.filter
def get_tag_value(tag):
    """Return tag meening on russian"""
    return dict(TAG_CHOICES)[tag]