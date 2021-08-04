from jtool.execution.registry import register_command
from jtool.execution import runprogram
from jtool.utils.errorhandling import assert_with_data, validate_re
from jtool.utils.func_asserts import lambda_type
import re


@register_command("unique")
def UNIQUE():
    '''selects unique values from list'''
    return lambda data: list(set(lambda_type(data, list)))


@register_command("refilter")
def RE_FILTER(filterspec):
    '''regexp filter with parameter (jtool_command=>regexp). 
    converts input to string, runs the optional jtool command to narrow down selection
    returns the input if the regular expression matches or None/null if it doesn't match'''
    assert_with_data("=>" in filterspec, filterspec,
                     "regexp filter must be in fhe form of selector=>regular_expression")
    fsplit = filterspec.split("=>")
    selector = fsplit[0]
    restr = fsplit[1]
    validate_re(restr)
    return lambda data: data if re.search(restr, str(runprogram(data, selector) if selector else data)) else None

def re_wrapper(regexp,data):
    test = re.search(regexp, data)
    if test:
        return test.group()


@register_command("refind")
def RE_FIND(regexp):
    '''returns the regular expression match for a given string'''
    return lambda data: re_wrapper(regexp, lambda_type(data, str))


@register_command("haskey")
def HASKEY(key):
    '''returns the json if it contains the given key'''
    return lambda data: data if (isinstance(data, dict) and key in data) else None
      