from django import template

register = template.Library()

@register.filter
def range_filter(value):
    return range(1, value + 1)

@register.filter
def range_to(value):
    return range(1, 6)  # Always return range from 1 to 5
