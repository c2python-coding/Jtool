from jtool.execution.registry import register_command
from jtool.utils.func_asserts import lambda_type


'''
Custom Commands

See README.md for explanation
'''


@register_command("keys")
def make_KEYS_op():
    '''returns the keys at the top level'''
    return lambda data: [x for x in lambda_type(data, dict)]


@register_command("values")
def make_VALUES_op():
    '''creates array from values of top level keys'''
    return lambda data: [data[key] for key in lambda_type(data, dict)]



@register_command("split")
def make_CONVERT_op():
    '''converts a key:value set to array of single key:value items, i.e {key1:val1,...} -> [{key1:val1},...]'''
    return lambda data: [{key: data[key]} for key in lambda_type(data, dict)]


