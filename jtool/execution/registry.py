from jtool.utils.errorhandling import raise_error, assert_with_data


CUSTOM_COMMANDS = {}
COMMAND_HELP_LIST = {}
CORE_COMMANDS = {}


def append_help_item(namespace,helpstring):
    if namespace not in COMMAND_HELP_LIST:
        COMMAND_HELP_LIST[namespace] = []
    COMMAND_HELP_LIST[namespace].append(helpstring)

def register_command(opname):
    ''' decorator for registering custom commands'''
    assert_with_data(opname not in CUSTOM_COMMANDS, opname, "duplicate operation name")
    def identity_dec(func, operation=opname):
        namespace = func.__module__.split(".")[-1]
        CUSTOM_COMMANDS[operation] = func
        if func.__code__.co_argcount > 0:
            pstring = "("+func.__code__.co_varnames[0]+")"
        else:
            pstring = "" 
        assert_with_data(func.__doc__, func,
                         "no description defined for custom function")
        append_help_item(namespace, "@" + opname + pstring + " : " + func.__doc__)
        return func
    return identity_dec


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
    is_iterator = False
    if escaped:
        return (CORE_COMMANDS[None](token), False)
    if token[0] == "*":
        is_iterator = True
        token = token[1:]
    if token[0] in CORE_COMMANDS:
        return (CORE_COMMANDS[token[0]](token), is_iterator)
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
                return (t_callable, is_iterator)
            else:
                raise_error(
                    token, "not a valid command (if you are trying to reference a key, escape it with ' or \" )")
        else:
            return (CORE_COMMANDS[None](token), is_iterator)
