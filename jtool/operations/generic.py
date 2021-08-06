from jtool.execution.registry import register_command
from jtool.utils.constants import canoncial_type_names


@register_command("count")
def COUNT_OP():
    '''counts number of elements in array or top level values in dict'''
    return lambda data: len(data)


@register_command("type")
def TYPE_OP():
    '''returns type of data'''
    return lambda data: canoncial_type_names[type(data)]


@register_command("delete")
def DELETE_OP(val):
    '''removes a entry from json by key'''
    return lambda data: data


@register_command("transform")
def DELETE_OP(val):
    '''removes a entry from json by key'''
    return lambda data: data