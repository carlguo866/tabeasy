from django import template
from itertools import chain

register = template.Library()

@register.filter(name='chr')
def chr_(value):
    return chr(value + 65)

@register.filter(name='add_array')
def add_array_(array1, array2):
    return list(chain(array1,array2))

@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)

from django import template

@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)
