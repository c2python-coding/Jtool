from jtool.execution.registry import register_command
from jtool.utils.func_asserts import lambda_type, exception_wrapper
import re

@register_command("splitlines")
def SPLITLINES_OP():
    '''splits the text by lines'''
    return lambda data: lambda_type(data, str).split("\n")


@register_command("resplit")
def SPLITLINES_OP(re_delimeter):
    '''splits the string by a delimeter and returns an array'''
    re_delimeter = re_delimeter.strip("'\"")
    splitlambda = lambda data, tkn=re_delimeter: re.split(tkn, lambda_type(data, str))
    return lambda instring: exception_wrapper(splitlambda, instring, "error splitting by regular expression")


@register_command("strip")
def STRIP_OP():
    '''removes leading/trailing spaces'''
    striplambda = lambda data: lambda_type(data, str).strip()
    return lambda instring: exception_wrapper(striplambda, instring, "error removing spaces")
