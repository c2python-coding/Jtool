#!/usr/bin/env python3
import json
import sys
import re
import argparse
from argparse import RawTextHelpFormatter

# TODO: Standardize validation routing during operation creation
# TODO: Generalize quote charaters to general escape
# TODO: timeout for read if debug
# TODO: more generic way of handling isiter

_DEFAULT_CMD = {}
_CUSTOM_CMD = {}
_CMD_HELP_LIST = []
_DEBUG_FLAG = False
_DEBUG_INDENT = ""

# --------------------HELPER COMMANDS ---------------------------------------------------------------------------------------------------------


def _type_check(data, ttype):
    if isinstance(data, ttype):
        return data
    raise AssertionError("data is not of " + str(ttype))


def _generic_check(data, chklambda, message):
    if chklambda(data):
        return data
    raise AssertionError(message)


def _membership_check(item, collection):
    if item in collection:
        return item
    collection_str = "collection"
    if isinstance(collection, list):
        collection_str = "list"
    if isinstance(collection, dict):
        collection_str = "dict"
    raise AssertionError(str(item) + " not in " + collection_str)


def _re_check(data, regexp, message):
    if re.search(regexp, data):
        return data
    raise AssertionError(message)


def _split_function_token(fulltoken):
    assert fulltoken[0] == "@", "function token must start with @"
    if fulltoken[-1] == ")":
        fulltoken = fulltoken[:-1]
        splitstr = fulltoken.split("(")
        tknname = splitstr[0][1:]
        tknparams = splitstr[1]
    else:
        tknname = fulltoken[1:]
        tknparams = None
    return(tknname, tknparams)

# -------------------- DEFAULT COMMANDS ------------------------------------------------------------------------------------


def _key_selector(token):
    return lambda data, tkn=token: _type_check(data, dict)[_membership_check(tkn, data)]


_CMD_HELP_LIST.append(
    "key : selects the particular key from the given top level json")

# --------------------

_ITER_OPERATOR = "*"
def _ITER_LAMBDA(val): return isinstance(val, list)


_DEFAULT_CMD[_ITER_OPERATOR] = lambda _: _ITER_LAMBDA
_CMD_HELP_LIST.append(
    _ITER_OPERATOR + " : applies next command iteratively on items in a list")


def isiterop(op, subval):
    if op == _ITER_LAMBDA:
        assert op(subval), "Iterators apply only to lists"
        return True
    return False

# --------------------


_IDENT_OPERATOR = "-"
def _IDENT_LAMBDA(val): return val


_DEFAULT_CMD[_IDENT_OPERATOR] = lambda _: _IDENT_LAMBDA
_CMD_HELP_LIST.append(
    _IDENT_OPERATOR + " : identity operator (returns the current selection without modification)")

# --------------------
_MULTI_KEY_OPERATOR = "{}"


def _multi_key_op(token):
    _re_check(token, r"\{[\w,]+\}",
              "multi key command must be in form {key1, key2 ...}")
    processed_keys = [key.strip() for key in token.strip("{}").split(",")]
    return lambda data, keyset=processed_keys: {_membership_check(key, _type_check(data, dict)): data[key] for key in keyset}


_DEFAULT_CMD[_MULTI_KEY_OPERATOR[0]] = lambda token: _multi_key_op(token)
_CMD_HELP_LIST.append(_MULTI_KEY_OPERATOR +
                      " : selects multiple keys from the current dictionary")

# --------------------

_ARRAY_OPERATOR = "[]"


def _array_op(token):
    _re_check(token, r"\[[0-9,-]+\]",
              "range specifier must be in form [0,1,2-3...]")
    rangestring = token.strip("[]")
    indicies = []
    crange = rangestring.split(",")
    for elem in crange:
        if "-" in elem:
            rangevals = elem.split("-")
            lval = int(rangevals[0].strip())
            rval = int(rangevals[1].strip())
            indicies += list(range(lval, rval+1))
        else:
            indicies.append(int(elem.strip()))
    if len(indicies) == 1:
        tidx = indicies[0]
        return lambda data, idx=tidx: _type_check(data, list)[idx]
    else:
        return lambda data, idxes=indicies: [_type_check(data, list)[i] for i in idxes]


_DEFAULT_CMD[_ARRAY_OPERATOR[0]] = lambda token: _array_op(token)
_CMD_HELP_LIST.append(
    _ARRAY_OPERATOR + " : selects range or particular indicies of arrays")


# -------------------- CUSTOM COMMANDS REGISTER -----------------------------------------------------------------------------

def op_registrar(opname):
    def identity_dec(func):
        _CUSTOM_CMD[opname] = func
        _CMD_HELP_LIST.append("@" + opname + " : " + func.__doc__)
        return func
    return identity_dec


# -------------------- CUSTOM COMMANDS ---------------------


@op_registrar("keys")
def make_KEYS_op(_):
    '''returns the keys at the top level'''
    return lambda data: [x for x in data]


@op_registrar("keys2array")
def make_VALUES_op(_):
    '''creates array from values of top level keys'''
    return lambda data: [data[key] for key in _type_check(data, dict)]


@op_registrar("flatten")
def make_COMBINE_op(_):
    '''combines list of lists into a list'''
    return lambda data: [c for subarray in _type_check(data, list) for c in _type_check(subarray, list)]


@op_registrar("unique")
def make_UNIQUE_op(_):
    '''selects unique values from list'''
    return lambda data: list(set(_type_check(data, list)))


@op_registrar("count")
def make_COUNT_op(_):
    '''counts number of elements in list or top level values in dict'''
    return lambda data: len(data)


@op_registrar("type")
def make_TYPE_op(_):
    '''returns type of data'''
    return lambda data: type(data).__name__


@op_registrar("refilter")
def make_FILTER_op(params):
    '''regexp filter on list based on the syntax (selector=>regular_expression)'''
    assert "=>" in params, "regexp filter must be in fhe form of selector=>regular_expression"
    fsplit = params.split("=>")
    selector = fsplit[0]
    restr = fsplit[1]
    return lambda data, slct=selector, regexp=restr: data if re.search(restr, str(selectfrom(data, slct))) else None

# --------------------  --------------------- -------------------- --------------------
_DESCRIPTION_STR = """ A tool for selecting json fields. Accepts a file or stdin as input
Syntax for the selector command string follows the dot (.) notaion, where commands
are separated by period.
For special characters in selectors or expressions,  you can use single/double quotes 
to avoid interpretation as a command
The following are valid commands. Some take arguments passed in ():

"""
_DESCRIPTION_STR += "\n".join("  "+x for x in _CMD_HELP_LIST)
parser = argparse.ArgumentParser(
    description=_DESCRIPTION_STR, formatter_class=RawTextHelpFormatter)
parser.add_argument("commandstr", help="json select command", nargs="?")
parser.add_argument("filename", help="filename", nargs="?")
parser.add_argument("-d", "--debug", action='store_true',
                    help="debug mode", required=False)
args = parser.parse_args()
if (args.debug):
    _DEBUG_FLAG = True


def get_operration_lambda(token, escaped=False):
    if escaped:
        return _key_selector(token)
    if token[0] in _DEFAULT_CMD:
        return _DEFAULT_CMD[token[0]](token)
    else:
        if token[0] == "@":
            (tknname, params) = _split_function_token(token)
            if tknname in _CUSTOM_CMD:
                return _CUSTOM_CMD[tknname](params)
            else:
                raise AssertionError(
                    tknname + "not a valid command (if you are trying to reference a key, escape it with ' or \" )")
        else:
            return _key_selector(token)


def parse_commands(tokenstr):
    global _DEBUG_FLAG
    global _DEBUG_INDENT
    operations = []
    command_strs = []
    if _DEBUG_FLAG:
        print(_DEBUG_INDENT, "received string:", tokenstr)
    assert tokenstr[0] != ".", "selection specifier can't start with ."
    idx = 0
    buffer = ""
    groupchar = None
    while idx < len(tokenstr):
        if groupchar:
            if tokenstr[idx] == groupchar:
                groupchar = None
            buffer += tokenstr[idx]
        else:
            if tokenstr[idx] == ".":
                command_strs.append(buffer)
                buffer = ""
            else:
                if tokenstr[idx] in ["'", "\""]:
                    groupchar = tokenstr[idx]
                elif tokenstr[idx] == "(":
                    groupchar = ")"
                buffer += tokenstr[idx]
        idx += 1
    assert not groupchar, f"mismatch quotes/parenthesis {groupchar}"
    if buffer:
        command_strs.append(buffer)
    if _DEBUG_FLAG:
        print(_DEBUG_INDENT, "Processed tokens:", str(command_strs))
    for tkn in command_strs:
        if (tkn[0] == "'" and tkn[-1] == "'") or (tkn[0] == "\"" and tkn[-1] == "\""):
            tkn_escaped = True
            tkn = tkn.strip("'\"")
        else:
            tkn_escaped = False
        if _DEBUG_FLAG:
            debug_escape = "(escaped)" if tkn_escaped else ""
            print(_DEBUG_INDENT, "Generating lambda for token", tkn, debug_escape)
        operations.append(get_operration_lambda(tkn))
    return (operations, command_strs)


def selectfrom(jsondata, parsestr):
    global _DEBUG_FLAG
    global _DEBUG_INDENT
    (operations, command_tokens) = parse_commands(parsestr)
    subval = jsondata
    while operations:
        op = operations.pop(0)
        if _DEBUG_FLAG:
            tokenop = command_tokens.pop(0)
            print(_DEBUG_INDENT, "Applying operation:", tokenop, op)
        if isiterop(op, subval):
            assert operations, "Cant apply iterator without a following command"
            nextop = operations.pop(0)
            if _DEBUG_FLAG:
                tokenop = command_tokens.pop(0)
                print(_DEBUG_INDENT, "Applying iterator operation:", tokenop, op)
                _DEBUG_INDENT += " "
            subval = [nextop(element) for element in subval]
            subval = [element for element in subval if element is not None]
            if _DEBUG_FLAG:
                _DEBUG_INDENT = _DEBUG_INDENT[:-1]
        else:
            subval = op(subval)
    return subval


if args.commandstr:
    parsestring = args.commandstr
    if args.filename:
        with open(args.filename, "r") as f:
            data = json.load(f)
    else:
        data = json.loads(sys.stdin.read())
    result = selectfrom(data, parsestring)
    if isinstance(result, str):
        print(result)
    else:
        print(json.dumps(result, indent=4))
