from django import template
from blog.models import Category


register = template.Library()


@register.inclusion_tag('blog/menu_tpl.html')
def show_menu(menu_class='menu'):
    category = Category.objects.all()
    return {"category": category, "menu_class": menu_class}