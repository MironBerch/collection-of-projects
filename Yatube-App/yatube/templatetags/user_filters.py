from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    """Function which filter forms field """
    return field.as_widget(attrs={'class': css})