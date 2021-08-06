from jtool.utils.errorhandling import raise_error, assert_with_data
from jtool.utils.debug import print_debug
from jtool.utils.text_utils import skip_quotes, q_chars
from inspect import signature

CUSTOM_COMMANDS = {}
COMMAND_HELP_LIST = {}
CORE_COMMANDS = {}


def append_help_item(namespace, helpstring):
    helparray = helpstring.split("\n")
    if len(helparray) > 1:
        helparray = [x.strip(" \t") for x in helparray]
        idx = helparray[0].find(":")+2
        helpstring = "\n".join(
            [helparray[0]] + [idx*" " + x for x in helparray[1:]])
    if namespace not in COMMAND_HELP_LIST:
        COMMAND_HELP_LIST[namespace] = []
    COMMAND_HELP_LIST[namespace].append(helpstring)


def register_command(opname):
    ''' decorator for registering custom commands'''
    assert_with_data(opname not in CUSTOM_COMMANDS,
                     opname, "duplicate operation name")
    assert_with_data(":" not in opname, opname, "opname cannot contain :")

    def identity_dec(func, operation=opname):
        namespace = func.__module__.split(".")[-1].upper()
        if len(signature(func).parameters) > 0:
            paramlist = [x for x in signature(func).parameters]
            nparams = len(paramlist)
            pstring = f"({','.join(paramlist)})"
        else:
            nparams = 0
            pstring = ""
        CUSTOM_COMMANDS[operation] = (func,nparams)
        assert_with_data(func.__doc__, str(func),
                         "no description defined for custom function")
        append_help_item(namespace, "@" + opname +
                         pstring + " : " + func.__doc__)
        return func
    return identity_dec

    

def param_processor(paramstring):
    idx = 0
    params = tuple()
    buffer = ""
    while idx < len(paramstring):
        tchar = paramstring[idx]
        if tchar in q_chars:
            eidx = skip_quotes(paramstring,idx)
            buffer += paramstring[idx+1:eidx]
            idx = eidx
        elif tchar == ",":
            if buffer:
                params += (buffer,)
            buffer = ""
        else:
            buffer += tchar
        idx+=1
    if buffer:
        params += (buffer,)
    return params
        

def split_function_token(fulltoken):
    assert_with_data(fulltoken[0] == "@", fulltoken,
                     "function token must start with @")
    if fulltoken[-1] == ")":
        fulltoken = fulltoken[:-1]
        splitstr = fulltoken.split("(")
        tknname = splitstr[0][1:]
        tknparams = param_processor(splitstr[1])
    else:
        tknname = fulltoken[1:]
        tknparams = tuple()
    paramdebug = ""
    if tknparams:
        paramdebug = f" with parameters({','.join(tknparams)})"
    print_debug("Parsed command", tknname + paramdebug)
    return(tknname, tknparams)


def get_operation_lambda(token, escaped=False):
    is_iterator = 0
    if escaped:
        return (CORE_COMMANDS[None](token), 0)
    while token[0] == "*":
        is_iterator += 1
        token = token[1:]
    if token[0] in CORE_COMMANDS:
        return (CORE_COMMANDS[token[0]](token), is_iterator)
    else:
        if token[0] == "@":
            (tknname, params) = split_function_token(token)
            if tknname in CUSTOM_COMMANDS:
                funobj = CUSTOM_COMMANDS[tknname][0]
                nparams = CUSTOM_COMMANDS[tknname][1]
                assert_with_data(nparams == len(params),token, f"incorrect number of parameters to @{tknname}, expecting {nparams}")
                try:
                    t_callable = funobj(*params) if params else funobj()
                except TypeError as e:
                    raise_error(token, str(
                        e)+", in operation generator function")
                assert_with_data(callable(
                    t_callable), token, "Returned operation for given token must be a callable (function or lambda)")
                return (t_callable, is_iterator)
            else:
                raise_error(
                    token, "not a valid command (if you are trying to reference a key, escape it with ' or \" )")
        else:
            return (CORE_COMMANDS[None](token), is_iterator)


    