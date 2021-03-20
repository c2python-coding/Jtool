from jtool.execution.registry import append_help_item, CORE_COMMANDS
from jtool.utils.errorhandling import assert_with_data, raise_error
from jtool.utils.func_asserts import lambda_member, lambda_type
import re

corens = "core operators"

def KEY_SELECT(token):
    return lambda data, tkn=token: lambda_type(data, dict)[lambda_member(tkn, data)]

append_help_item(corens, "key : returns the value for particular key")

CORE_COMMANDS[None] = KEY_SELECT

# --------------------
MULTI_KEY_OPERATOR = "{}"


def MULTI_KEY_SELECT(token):
    assert_with_data(re.search(r"\{[\w,]+\}", token), token,
                     "multi key command must be in form {key1, key2 ...}")
    processed_keys = [key.strip() for key in token.strip("{}").split(",")]
    return lambda data, keyset=processed_keys: {lambda_member(key, lambda_type(data, dict)): data[key] for key in keyset}


CORE_COMMANDS[MULTI_KEY_OPERATOR[0]
                 ] = MULTI_KEY_SELECT
append_help_item(corens, MULTI_KEY_OPERATOR + " : returns values for multiple keys")

# --------------------

ARRAY_OPERATOR = "[]"


def ARRAY_SELECT(token):
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


CORE_COMMANDS[ARRAY_OPERATOR[0]
                 ] = ARRAY_SELECT
append_help_item(corens, ARRAY_OPERATOR + " : selects range or particular indicies of arrays [0,1,2-4,...]")

# -------------------------

ITER_OPERATOR = "*"

append_help_item(corens, ITER_OPERATOR + " : prepend to command to apply iteravely on a list or each key:value pair")

# --------------------
