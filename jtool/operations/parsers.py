from jtool.execution.registry import register_command
from jtool.utils.func_asserts import lambda_type, exception_wrapper
import json


@register_command("json")
def parse_into_json():
    '''parsers data into json'''
    str2json = lambda data: json.loads(data)
    return lambda strdata: exception_wrapper(str2json, lambda_type(strdata, str), "could not parse input into json")
