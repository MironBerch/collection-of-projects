from atexit import register
from django import template


register = template.Library()


@register.filter
def count_calc(field):
    """Count recipes on the following page"""
    result = str(int(field) - 3)
    if result[-1] == '1':
        return f'{result} рецепт...'
    elif result[-1] in ['2', '3', '4']:
        return f'{result} рецепта...'
    else:
        return f'{result} рецептов...'