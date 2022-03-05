from django import template

register = template.Library()

@register.filter
def modulo(num, val):
    return num % val

@register.filter
def subtract(value, arg):
    return value - arg

@register.simple_tag
def get_row_colour(counter):
    if counter%2 == 0:
        return "table-info"
    else:
        return "table-warning"