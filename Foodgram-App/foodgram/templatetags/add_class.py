from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    """Add field class for input form"""
    return field.as_widget(attrs={'class': css})


@register.filter
def class_tag(tag):
    """Return required field class for buttons on/off tag"""
    classes = {
        'breakfast': 'badge badge_style_orange',
        'lunch': 'badge badge_style_green',
        'dinner': 'badge badge_style_purple',
    }

    return classes[tag]