from jtool.execution.registry import register_command
from jtool.utils.func_asserts import lambda_type, exception_wrapper, lambda_multi_type
from jtool.utils.errorhandling import raise_error
import json


@register_command("asjson")
def parse_into_json():
    '''convert data into json'''
    def json2str(data): return json.dumps(data, indent=4)
    return lambda dictdata: exception_wrapper(json2str, lambda_multi_type(dictdata, list, dict), "could not convert data to json")


@register_command("asjson_indent")
def parse_into_json(indent):
    '''convert data into json with indent specified in the argument'''
    try:
        indentval = int(indent)
    except Exception:
        raise_error(indent, "not a valid indent, must be an integer")

    def json2str(data): return json.dumps(data, indent=indentval)
    return lambda dictdata: exception_wrapper(json2str, lambda_multi_type(dictdata, list, dict), "could not convert data to json")


@register_command("ascompactjson")
def parse_into_json():
    '''convert data into json with no spaces'''
    def json2str(data): return json.dumps(data, separators=(',', ":"))
    return lambda dictdata: exception_wrapper(json2str, lambda_multi_type(dictdata, list, dict), "could not convert data to json")
