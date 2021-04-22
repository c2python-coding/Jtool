from jtool.execution.registry import register_command
from jtool.utils.func_asserts import lambda_type, exception_wrapper
from jtool.utils.markup_utils import parse_html
from jtool.utils.csv_utils import parse_csv
from jtool.utils.errorhandling import assert_with_data
import json


@register_command("json")
def PARSE_INTO_JSON():
    '''parsers data as json, into referensable structure with key:value pairs and array indexing'''
    str2json = lambda data: json.loads(data)
    return lambda strdata: exception_wrapper(str2json, lambda_type(strdata, str), "could not parse input into json")


@register_command("markup")
def PARSE_INTO_MARKUP():
    '''parses data as html/xhtml/xml into a json like structure
    each tag is a json object, with keys of  <tag> for type and <innerHTML>
    for its children, and key:value pairs for attributes'''
    return lambda data: parse_html(data)

@register_command("csv")
def PARSE_INTO_MARKUP(delim):
    '''parses data into csv based on the delimeter specified in delim
    assumes double quotes are used to escape the data'''
    return lambda data: parse_csv(data, delim)
