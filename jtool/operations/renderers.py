from jtool.execution.registry import register_command
from jtool.utils.func_asserts import exception_wrapper, lambda_type
from jtool.utils.errorhandling import raise_error
from jtool.utils.markup_utils import to_html
from jtool.utils.constants import PRETTY_INDENT as p_ind
import json
import re


@register_command("tojson")
def RENDER_JSON():
    '''convert json data into formatted json output
    This is generally needed for json as default string output uses single quotes'''
    json2str = lambda data: json.dumps(data, indent=p_ind)
    return lambda dictdata: exception_wrapper(json2str, lambda_type(dictdata, list, dict), "tojson")


@register_command("tojson_indent")
def RENDER_JSON_INDENT(indent):
    '''convert json data into formatted json with indent specified in the argument'''
    try:
        indentval = int(indent)
    except Exception:
        raise_error(indent, "not a valid indent, must be an integer")
    json2str = lambda data: json.dumps(data, indent=indentval)
    return lambda dictdata: exception_wrapper(json2str, lambda_type(dictdata, list, dict), "tojson_indent")


@register_command("tocompact_json")
def RENDER_COMPACT_JSON():
    '''convert json data into json with no spaces'''
    json2str = lambda data: json.dumps(data, separators=(',', ":"))
    return lambda dictdata: exception_wrapper(json2str, lambda_type(dictdata, list, dict), "tocompact_json")


@register_command("tomarkup")
def parse_into_markup():
    '''convert markup specific json data into markup format'''
    return lambda mjson: to_html(mjson)

def compact_markup(htmldata):
    htmldata = htmldata.replace("\n", " ")
    htmldata = re.sub("> +<", "><", htmldata)
    return htmldata


@register_command("tocompactmarkup")
def RENDER_COMPACT_MARKUP():
    '''convert markup specific json data into compatct-ish markup format'''
    return lambda mjson: compact_markup(to_html(mjson))

@register_command("tomultiline")
def RENDER_MULTILINE():
    '''convert array of strings into a text output with each item on newline'''
    return lambda ldata: "\n".join(x for x in lambda_type(ldata, list))


@register_command("tocsv")
def RENDER_CSV(delim):
    '''converts arrays or nested arrays into csv output with given delimeter'''
    text_format = lambda text: str(text).replace("'", "\\\"").replace("\"", "\\\"")
    dimupsize = lambda ldata: ldata if isinstance(lambda_type(ldata, list)[0],list) else [ldata]
    return lambda ldata: "\n".join(delim.join(text_format(item) for item in lambda_type(line, list)) for line in dimupsize(ldata))

@register_command("to text")
def RENDER_TEXT():
    '''converts any data to string, usefull for rendering json or lists to text'''
    return lambda data: str(data)