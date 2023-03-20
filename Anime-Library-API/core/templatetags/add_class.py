from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    """Add field class for input form"""
    return field.as_widget(attrs={'class': css})