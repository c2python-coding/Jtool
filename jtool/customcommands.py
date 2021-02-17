from .commandregistry import register_command
from .helpers import type_assert
from .processing import selectfrom
import re

'''
Custom Commands

See README.md for explanation
'''


@register_command("keys")
def make_KEYS_op(_):
    '''returns the keys at the top level'''
    return lambda data: [x for x in data]


@register_command("keys2array")
def make_VALUES_op(_):
    '''creates array from values of top level keys'''
    return lambda data: [data[key] for key in type_assert(data, dict)]


@register_command("flatten")
def make_COMBINE_op(_):
    '''combines list of lists into a list'''
    return lambda data: [c for subarray in type_assert(data, list) for c in type_assert(subarray, list)]


@register_command("unique")
def make_UNIQUE_op(_):
    '''selects unique values from list'''
    return lambda data: list(set(type_assert(data, list)))


@register_command("count")
def make_COUNT_op(_):
    '''counts number of elements in list or top level values in dict'''
    return lambda data: len(data)


@register_command("type")
def make_TYPE_op(_):
    '''returns type of data'''
    return lambda data: type(data).__name__


@register_command("refilter")
def make_FILTER_op(params):
    '''regexp filter on list based on the syntax (selector=>regular_expression)'''
    assert "=>" in params, "regexp filter must be in fhe form of selector=>regular_expression"
    fsplit = params.split("=>")
    selector = fsplit[0]
    restr = fsplit[1]
    return lambda data, slct=selector, regexp=restr: data if re.search(restr, str(selectfrom(data, slct))) else None
