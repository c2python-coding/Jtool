from jtool.execution.registry import register_command
from jtool.utils.func_asserts import lambda_type, lambda_multi_type


@register_command("len")
def LENGTH_OP():
    '''length of element'''
    return lambda data: len(lambda_multi_type(data, list, dict))


@register_command("flatten")
def COMBINE_OP():
    '''combines list of lists into a list'''
    return lambda data: [c for subarray in lambda_type(data, list) for c in lambda_type(subarray, list)]

