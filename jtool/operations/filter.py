from jtool.execution.registry import register_command
from jtool.execution import runprogram
from jtool.utils.errorhandling import assert_with_data
from jtool.utils.func_asserts import lambda_type
import re


@register_command("unique")
def UNIQUE():
    '''selects unique values from list'''
    return lambda data: list(set(lambda_type(data, list)))

@register_command("refilter")
def RE_FILTER(filterspec):
    '''regexp filter with parameter (jtool_command=>regexp). 
    converts input to string, runs the processing commands in jtool_command, 
    and applies the regular expression filter regexp'''
    assert_with_data("=>" in filterspec, filterspec,
                     "regexp filter must be in fhe form of selector=>regular_expression")
    fsplit = filterspec.split("=>")
    selector = fsplit[0]
    restr = fsplit[1]
    return lambda data: data if re.search(restr, str(runprogram(data, selector) if selector else data)) else None


@register_command("haskey")
def HASKEY(key):
    '''returns the json if it contains the given key'''
    return lambda data: data if (isinstance(data, dict) and key in data) else None
      