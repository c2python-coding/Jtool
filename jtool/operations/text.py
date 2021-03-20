from jtool.execution.registry import register_command
from jtool.utils.func_asserts import lambda_type, exception_wrapper
import re

@register_command("splitlines")
def SPLITLINES_OP():
    '''counts number of elements in list or top level values in dict'''
    return lambda data: lambda_type(data, str).split("\n")


@register_command("splitstring")
def SPLITLINES_OP(re_delimeter):
    '''counts number of elements in list or top level values in dict'''
    re_delimeter = re_delimeter.strip("'\"")
    splitlambda = lambda data, tkn=re_delimeter: re.split(tkn, lambda_type(data, str))
    return lambda instring: exception_wrapper(splitlambda, instring, "error splitting by regular expression")
