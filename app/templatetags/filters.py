from django import template

register = template.Library()

@register.filter(is_safe=True)
def int_filter(value):
    try:
        return int(value)
    except ValueError:
        return None

@register.filter(is_safe=True)
def float_filter(value):
    try:
        return float(value)
    except ValueError:
        return None


