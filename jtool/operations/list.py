from jtool.execution.registry import register_command
from jtool.utils.func_asserts import lambda_type


@register_command("len")
def LENGTH_OP():
    '''length of array'''
    return lambda data: len(lambda_type(data, list, dict))


@register_command("flatten")
def FLATTEN_OP():
    '''combines array of arrays into a array'''
    return lambda data: [c for subarray in lambda_type(data, list) for c in lambda_type(subarray, list)]

@register_command("concat")
def CONCAT_OP(delimeter):
    '''combines array of items into a string with string representations of each item and a given delimeter'''
    return lambda data: delimeter.join([str(x) for x in lambda_type(data, list)])

@register_command("clean")
def CLEAN_OP():
    '''removes None and empty strings from array'''
    return lambda data: [x for x in lambda_type(data, list) if x]

