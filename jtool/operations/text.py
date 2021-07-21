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
    return lambda instring: exception_wrapper(striplambda, instring, "error removing leading/trailing spaces")


@register_command("prepend")
def PREPEND_OP(string):
    '''add text to beggining'''
    textlambda = lambda data, txt=string: txt + lambda_type(data, str)
    return lambda instring: exception_wrapper(textlambda, instring, "error prepending text")


@register_command("append")
def APPEND_OP(string):
    '''add text to the end'''
    textlambda = lambda data, txt=string:  lambda_type(data, str) + txt
    return lambda instring: exception_wrapper(textlambda, instring, "error appending text")

@register_command("remove")
def REMOVE_OP(string):
    '''removes text'''
    textlambda = lambda data, txt=string:  lambda_type(data, str).replace(string,"")
    return lambda instring: exception_wrapper(textlambda, instring, "error removing text")

@register_command("replace")
def REPLACE_OP(string):
    '''replaces text, argument in the form of (searchtext,replacetext)
    if comma character is desired to be searched or replaced, use %comma% in place
    if parethesis characters are desired, use %pl% or %pr% for ( and ) respectively'''
    args = [x.replace("%comma%",",").replace("%pl%","(").replace("%pr%",")") for x in string.split(",")]
    textlambda = lambda data, repspec=args:  lambda_type(data, str).replace(repspec[0],repspec[1])
    return lambda instring: exception_wrapper(textlambda, instring, "error replacing text")
