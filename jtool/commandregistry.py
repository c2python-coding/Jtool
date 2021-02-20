from .func_asserts import lambda_type, lambda_member, lambda_error
from .utils import assert_with_data, raise_error
import re

CUSTOM_COMMANDS = {}
COMMAND_HELP_LIST = []
DEFAULT_COMMANDS = {}


# DEFAULT COMMANDS--------

def KEY_SELECTOR(token):
    return lambda data, tkn=token: lambda_type(data, dict)[lambda_member(tkn, data)]


COMMAND_HELP_LIST.append(
    "key : selects the particular key from the given top level json")


# --------------------
MULTI_KEY_OPERATOR = "{}"


def MULTI_KEY_SELECT_OPERATION(token):
    assert_with_data(re.search(r"\{[\w,]+\}", token), token,
                     "multi key command must be in form {key1, key2 ...}")
    processed_keys = [key.strip() for key in token.strip("{}").split(",")]
    return lambda data, keyset=processed_keys: {lambda_member(key, lambda_type(data, dict)): data[key] for key in keyset}


DEFAULT_COMMANDS[MULTI_KEY_OPERATOR[0]
                 ] = lambda token: MULTI_KEY_SELECT_OPERATION(token)
COMMAND_HELP_LIST.append(
    MULTI_KEY_OPERATOR + " : selects multiple keys from the current dictionary")

# --------------------

ARRAY_OPERATOR = "[]"


def ARRAY_SELECT_OPERATION(token):
    assert_with_data(re.search(r"\[[0-9,-]+\]", token), token,
                     "range specifier must be in form [0,1,2-3...]")
    rangestring = token.strip("[]")
    indicies = []
    crange = rangestring.split(",")
    for elem in crange:
        try:
            if "-" in elem:
                rangevals = elem.split("-")
                lval = int(rangevals[0].strip())
                rval = int(rangevals[1].strip())
                indicies += list(range(lval, rval+1))
            else:
                indicies.append(int(elem.strip()))
        except Exception:
            raise_error(token, "invalid array selection specifier")
    if len(indicies) == 1:
        tidx = indicies[0]
        return lambda data, idx=tidx: lambda_type(data, list)[idx]
    else:
        return lambda data, idxes=indicies: [lambda_type(data, list)[i] for i in idxes]


DEFAULT_COMMANDS[ARRAY_OPERATOR[0]
                 ] = lambda token: ARRAY_SELECT_OPERATION(token)
COMMAND_HELP_LIST.append(
    ARRAY_OPERATOR + " : selects range or particular indicies of arrays [0,1,2-4,...]")

# -------------------------

ITER_OPERATOR = "*"

def ITER_OPERATION(token):
    assert_with_data(len(token) == 1, token,
                     "iteration operator sequencemust be in the form of '*.command_to_iterate'")
    return lambda data: data if (isinstance(data, list) or isinstance(data, dict)) \
        else lambda_error(data, "cant apply iterator on non json structure")


DEFAULT_COMMANDS[ITER_OPERATOR] = lambda token: ITER_OPERATION(token)
COMMAND_HELP_LIST.append(
    ITER_OPERATOR + " : applies the next command iteratively on items in a list")

# --------------------


def register_command(opname):
    ''' decorator for registering custom commands'''
    def identity_dec(func, operation=opname):
        CUSTOM_COMMANDS[operation] = func
        assert_with_data(func.__doc__, func,
                         "no description defined for custom function")
        COMMAND_HELP_LIST.append("@" + opname + " : " + func.__doc__)
        return func
    return identity_dec

# --------------------


def split_function_token(fulltoken):
    assert_with_data(fulltoken[0] == "@", fulltoken,
                     "function token must start with @")
    if fulltoken[-1] == ")":
        fulltoken = fulltoken[:-1]
        splitstr = fulltoken.split("(")
        tknname = splitstr[0][1:]
        tknparams = splitstr[1]
    else:
        tknname = fulltoken[1:]
        tknparams = None
    return(tknname, tknparams)


def get_operation_lambda(token, escaped=False):
    if escaped:
        return KEY_SELECTOR(token)
    if token[0] in DEFAULT_COMMANDS:
        return DEFAULT_COMMANDS[token[0]](token)
    else:
        if token[0] == "@":
            (tknname, params) = split_function_token(token)
            if tknname in CUSTOM_COMMANDS:
                try:
                    t_callable = CUSTOM_COMMANDS[tknname](
                        params) if params else CUSTOM_COMMANDS[tknname]()
                except TypeError as e:
                    raise_error(token, str(e))
                assert_with_data(callable(
                    t_callable), t_callable, "Returned operation must be a callable (function or lambda)")
                return t_callable
            else:
                raise_error(
                    token, "not a valid command (if you are trying to reference a key, escape it with ' or \" )")
        else:
            return KEY_SELECTOR(token)
