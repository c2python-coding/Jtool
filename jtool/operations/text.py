from jtool.execution.registry import register_command
from jtool.utils.text_utils import validate_re
from jtool.utils.func_asserts import lambda_type, exception_wrapper

@register_command("splitlines")
def SPLITLINES_OP():
    '''splits the text by lines'''
    return lambda data: lambda_type(data, str).split("\n")


@register_command("resplit")
def SPLITRE_OP(re_delimeter):
    '''splits the string by a delimeter and returns an array'''
    validate_re(re_delimeter)
    splitlambda = lambda data, tkn=re_delimeter: re.split(tkn, lambda_type(data, str))
    return lambda instring: exception_wrapper(splitlambda, instring, "resplit")

@register_command("charsplit")
def CHARSPLIT_OP():
    '''splits a string by characters'''
    makelist = lambda text: list(lambda_type(text,str))
    return lambda text: exception_wrapper(makelist,text,"charsplit")


@register_command("strip")
def STRIP_OP():
    '''removes leading/trailing spaces'''
    striplambda = lambda data: lambda_type(data, str).strip()
    return lambda instring: exception_wrapper(striplambda, instring, "strip")


@register_command("prepend")
def PREPEND_OP(string):
    '''add text to beginning'''
    textlambda = lambda data, txt=string: txt + lambda_type(data, str)
    return lambda instring: exception_wrapper(textlambda, instring, "prepend")


@register_command("append")
def APPEND_OP(string):
    '''add text to the end'''
    textlambda = lambda data, txt=string:  lambda_type(data, str) + txt
    return lambda instring: exception_wrapper(textlambda, instring, "append")

@register_command("remove")
def REMOVE_OP(string):
    '''removes text'''
    textlambda = lambda data, txt=string:  lambda_type(data, str).replace(string,"")
    return lambda instring: exception_wrapper(textlambda, instring, "remove")

@register_command("replace")
def REPLACE_OP(regexp,replace):
    '''searches text on the provided regular expressions and replaces every occurence'''
    validate_re(regexp)
    textlambda = lambda data, repspec=[regexp,replace]: re.sub(repspec[0],repspec[1],lambda_type(data, str))
    return lambda instring: exception_wrapper(textlambda, instring, "replace")
