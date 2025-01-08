from django import template

register = template.Library()

@register.filter
def key(dictionary, key):
    return dictionary.get(key)