from jtool.execution.registry import register_command
from jtool.utils.func_asserts import lambda_type


'''
Custom Commands

See README.md for explanation
'''


@register_command("keys")
def KEYS_OP():
    '''returns the keys in an array'''
    return lambda data: [x for x in lambda_type(data, dict)]


@register_command("values")
def VALUES_OP():
    '''returns an array of values of top level keys'''
    return lambda data: [data[key] for key in lambda_type(data, dict)]


@register_command("split")
def SPLIT_OP():
    '''converts a key:value set to array of single key:value items, i.e {key1:val1,...} -> [{key1:val1},...]'''
    return lambda data: [{key: data[key]} for key in lambda_type(data, dict)]


@register_command("remove")
def REMOVE_OP(key):
    '''removes a entry from json by key'''
    return lambda data: [{key: data[key]} for key in lambda_type(data, dict)]