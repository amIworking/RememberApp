from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name="range")

def range(value, first=0):
    res = []
    i = first
    while i < value:
        i+=1
        res.append(i)
    return res