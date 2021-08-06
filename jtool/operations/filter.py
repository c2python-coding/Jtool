from jtool.execution.registry import register_command
from jtool.execution import runprogram
from jtool.utils.text_utils import validate_re
from jtool.utils.func_asserts import lambda_type
import re


@register_command("unique")
def UNIQUE():
    '''selects unique values from list'''
    return lambda data: list(set(lambda_type(data, list)))


@register_command("refilter")
def RE_FILTER(selector,regexp):
    '''filters a subselection 
    The selector argument is a valid jtool selection command, while the regexp is the filter
    To filture current argument without selection, use (~,regexp) as arguments
    Note that the selector command applies the same format of data as in the output from
    the previous opreation, i.e no parser application is necessary
    '''
    validate_re(regexp)
    return lambda data: data if re.search(regexp, str(runprogram(data, selector) if selector else data)) else None


def re_wrapper(regexp,data):
    test = re.search(regexp, data)
    if test:
        return test.group()

@register_command("refind")
def RE_FIND(regexp):
    '''returns the regular expression match for a given string'''
    validate_re(regexp)
    return lambda data: re_wrapper(regexp, lambda_type(data, str))


@register_command("haskey")
def HASKEY(key):
    '''returns the json if it contains the given key'''
    return lambda data: data if (isinstance(data, dict) and key in data) else None
      