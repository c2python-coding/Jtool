from .helpers import type_assert, membership_assert, re_assert

CUSTOM_COMMANDS = {}
COMMAND_HELP_LIST = []
DEFAULT_COMMANDS = {}


# DEFAULT COMMANDS--------

def KEY_SELECTOR(token):
    return lambda data, tkn=token: type_assert(data, dict)[membership_assert(tkn, data)]


COMMAND_HELP_LIST.append(
    "key : selects the particular key from the given top level json")

# --------------------

IDENT_OPERATOR = "-"
def IDENT_FUN(val): return val


DEFAULT_COMMANDS[IDENT_OPERATOR] = lambda _: IDENT_FUN
COMMAND_HELP_LIST.append(
    IDENT_OPERATOR + " : identity operator (returns the current selection without modification)")

# --------------------
MULTI_KEY_OPERATOR = "{}"


def MULTI_KEY_SELECT_OPERATION(token):
    re_assert(token, r"\{[\w,]+\}",
              "multi key command must be in form {key1, key2 ...}")
    processed_keys = [key.strip() for key in token.strip("{}").split(",")]
    return lambda data, keyset=processed_keys: {membership_assert(key, type_assert(data, dict)): data[key] for key in keyset}


DEFAULT_COMMANDS[MULTI_KEY_OPERATOR[0]
                 ] = lambda token: MULTI_KEY_SELECT_OPERATION(token)
COMMAND_HELP_LIST.append(
    MULTI_KEY_OPERATOR + " : selects multiple keys from the current dictionary")

# --------------------

ARRAY_OPERATOR = "[]"


def ARRAY_SELECT_OPERATION(token):
    re_assert(token, r"\[[0-9,-]+\]",
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
        return lambda data, idx=tidx: type_assert(data, list)[idx]
    else:
        return lambda data, idxes=indicies: [type_assert(data, list)[i] for i in idxes]


DEFAULT_COMMANDS[ARRAY_OPERATOR[0]
                 ] = lambda token: ARRAY_SELECT_OPERATION(token)
COMMAND_HELP_LIST.append(
    ARRAY_OPERATOR + " : selects range or particular indicies of arrays [0,1,2-4,...]")

# -------------------------


ITER_OPERATOR = "*"
def ITER_CHECK(val): type_assert(val, list)


DEFAULT_COMMANDS[ITER_OPERATOR] = lambda _: ITER_CHECK
COMMAND_HELP_LIST.append(
    ITER_OPERATOR + " : applies the next command iteratively on items in a list")

# --------------------


def is_iter_operation(op, subval):
    if op == ITER_CHECK:
        op(subval)
        return True
    return False


def register_command(opname):
    ''' decorator for registering custom commands'''
    def identity_dec(func):
        CUSTOM_COMMANDS[opname] = func
        COMMAND_HELP_LIST.append("@" + opname + " : " + func.__doc__)
        return func
    return identity_dec


def split_function_token(fulltoken):
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


def get_operation_lambda(token, escaped=False):
    if escaped:
        return KEY_SELECTOR(token)
    if token[0] in DEFAULT_COMMANDS:
        return DEFAULT_COMMANDS[token[0]](token)
    else:
        if token[0] == "@":
            (tknname, params) = split_function_token(token)
            if tknname in CUSTOM_COMMANDS:
                t_callable = CUSTOM_COMMANDS[tknname](params)
                assert callable(t_callable), "Returned operation must be a callable (function or lambda)"
            else:
                raise AssertionError(
                    tknname + "not a valid command (if you are trying to reference a key, escape it with ' or \" )")
        else:
            return KEY_SELECTOR(token)
