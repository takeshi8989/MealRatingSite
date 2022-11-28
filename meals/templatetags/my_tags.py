
from django import template

register = template.Library()


@register.filter
def replace(value, arg):
    return value.replace(arg + "+", "")


@register.filter
def add(value, arg):
    return value + arg + "+"

@register.filter
def roundValue(value, arg):
    return  round(value, arg)

