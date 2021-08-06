from jtool.execution.registry import register_command
from jtool.utils.constants import canoncial_type_names
from jtool.utils.errorhandling import raise_error
from jtool.utils.func_asserts import lambda_in_range, lambda_member
import copy
import re


@register_command("count")
def COUNT_OP():
    '''counts number of elements in array or top level values in dict'''
    return lambda data: len(data)


@register_command("type")
def TYPE_OP():
    '''returns type of data'''
    return lambda data: canoncial_type_names[type(data)]


def delete_handler(item, key):
    #indicies
    try:
        numval = int(key)
        if isinstance(item,dict):
            raise_error(item, "@delete: cant delete numerical index in json")
        indicies = [numval]
        combine_string = False
        if isinstance(item, str):
            dcopy = list(item)
            combine_string = True
        else:
            dcopy = copy.deepcopy(item)
        for x in indicies:
            lambda_in_range(x, item)
            dcopy.pop(x)
        if combine_string:
            dcopy = "".join(x for x in dcopy)
        return dcopy
    except ValueError:
        pass
    #keys
    if not isinstance(item,dict):
        raise_error(item, "@delete: cant delete string key on non json")
    lambda_member(key,item)
    dcopy = copy.deepcopy(item)
    dcopy.pop(key)
    return dcopy  


@register_command("delete")
def DELETE_OP(val):
    '''deletes index in array or string, or key in a json specified in value'''
    return lambda data, idx=val: delete_handler(data,idx)


@register_command("transform")
def TRANSFORM_OP(val):
    '''TODO'''
    return lambda data: data