from jtool.execution.registry import register_command
from jtool.utils.func_asserts import exception_wrapper, lambda_type
from jtool.utils.errorhandling import raise_error
from jtool.utils.markup_utils import to_html
from jtool.utils.constants import PRETTY_INDENT as p_ind
import json
import re


@register_command("asjson")
def parse_into_json():
    '''convert data into json'''
    json2str = lambda data: json.dumps(data, indent=p_ind)
    return lambda dictdata: exception_wrapper(json2str, lambda_type(dictdata, list, dict), "could not convert data to json")


@register_command("asjson_indent")
def parse_into_json_indent(indent):
    '''convert data into json with indent specified in the argument'''
    try:
        indentval = int(indent)
    except Exception:
        raise_error(indent, "not a valid indent, must be an integer")
    json2str = lambda data: json.dumps(data, indent=indentval)
    return lambda dictdata: exception_wrapper(json2str, lambda_type(dictdata, list, dict), "could not convert data to json")


@register_command("ascompactjson")
def parse_into_compact_json():
    '''convert data into json with no spaces'''
    json2str = lambda data: json.dumps(data, separators=(',', ":"))
    return lambda dictdata: exception_wrapper(json2str, lambda_type(dictdata, list, dict), "could not convert data to json")


@register_command("asmarkup")
def parse_into_markup():
    '''convert data into markup format'''
    return lambda mjson: to_html(mjson)

def compact_markup(htmldata):
    htmldata = htmldata.replace("\n", " ")
    htmldata = re.sub("> +<", "><", htmldata)
    return htmldata


@register_command("ascompactmarkup")
def parse_into_compact_markup():
    '''convert data into compatct-ish markup format'''
    return lambda mjson: compact_markup(to_html(mjson))
