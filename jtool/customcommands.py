from .commandregistry import register_command
from .func_asserts import lambda_type
from .processing import selectfrom
from .utils import assert_with_data
import re

'''
Custom Commands

See README.md for explanation
'''


@register_command("keys")
def make_KEYS_op():
    '''returns the keys at the top level'''
    return lambda data: [x for x in data]


@register_command("values")
def make_VALUES_op():
    '''creates array from values of top level keys'''
    return lambda data: [data[key] for key in lambda_type(data, dict)]


@register_command("json2array")
def make_CONVERT_op():
    '''converts a json to array of single key jsons, i.e {key1:val1,...} -> [{key1:val1},...]'''
    return lambda data: [{key: data[key]} for key in lambda_type(data, dict)]


@register_command("flatten")
def make_COMBINE_op():
    '''combines list of lists into a list'''
    return lambda data: [c for subarray in lambda_type(data, list) for c in lambda_type(subarray, list)]


@register_command("unique")
def make_UNIQUE_op():
    '''selects unique values from list'''
    return lambda data: list(set(lambda_type(data, list)))


@register_command("count")
def make_COUNT_op():
    '''counts number of elements in list or top level values in dict'''
    return lambda data: len(data)


@register_command("type")
def make_TYPE_op():
    '''returns type of data'''
    return lambda data: type(data).__name__


@register_command("refilter")
def make_FILTER_op(params):
    '''regexp filter on list based on the syntax (selector=>regular_expression)'''
    assert_with_data("=>" in params, params,
                     "regexp filter must be in fhe form of selector=>regular_expression")
    fsplit = params.split("=>")
    selector = fsplit[0]
    restr = fsplit[1]
    return lambda data, slct=selector, regexp=restr: data if re.search(restr, str(selectfrom(data, slct) if slct else data)) else None
