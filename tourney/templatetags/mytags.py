import math
import random

from django import template
from itertools import chain

from django.core.exceptions import ValidationError

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

@register.filter(name='round_opponent')
def round_opponent_(team, round_num):
  return team.round_opponent(round_num)

@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)

@register.simple_tag
def get_competitor(subsection_list, subsection):
    if subsection_list.filter(subsection=subsection).exists():
        return subsection_list.get(subsection=subsection).competitor
    else:
        return None

@register.simple_tag
def get_character(subsection_list, section):
    if subsection_list.filter(subsection__type='direct', subsection__role='wit',
                           subsection__section=section).exists():
        return subsection_list.get(subsection__type='direct',subsection__role='wit',
                                        subsection__section=section).character
    else:
        return None

# @register.simple_tag
# def get_character_pronouns(subsection_list, section):
#     character = get_character(subsection_list, section)
#     if character:




@register.filter(name='int_str')
def int_str(val):
    keyspace = "fw59eorpma2nvxb07liqt83_u6kgzs41-ycdjh"
    """ Turn a positive integer into a string. """
    assert val >= 0
    val = chaffify(val)
    out = ""
    while val > 0:
        val, digit = divmod(val, len(keyspace))
        out += keyspace[digit]

    return out[::-1]

def chaffify(val, chaff_size = 150, chaff_modulus = 7):
    """ Add chaff to the given positive integer.
    chaff_size defines how large the chaffing value is; the larger it is, the larger (and more unwieldy) the resulting value will be.
    chaff_modulus defines the modulus value for the chaff integer; the larger this is, the less chances there are for the chaff validation in dechaffify() to yield a false "okay".
    """
    chaff = random.randint(0, math.floor(chaff_size / chaff_modulus)) * chaff_modulus
    return val * chaff_size + chaff


role_choices = [
    ('att', 'attorneys'),
    ('wit', 'witnesses')
]

@register.filter
def display_role(q):
    for choice in role_choices:
        if choice[0] == q:
            return choice[1]
    return ''
