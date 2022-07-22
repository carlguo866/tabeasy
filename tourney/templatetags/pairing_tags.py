from django import template

register = template.Library()

@register.filter(name='chr')
def chr_(value):
    return chr(value + 65)

