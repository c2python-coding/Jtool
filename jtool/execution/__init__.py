from .registry import get_operation_lambda
from jtool.utils.errorhandling import raise_error, assert_with_data
from jtool.utils.debug import print_debug
from jtool.utils.text_utils import q_chars,skip_quotes,match_bracket

class OperationToken:

    def __init__(self, tkn):
        self.token = tkn
        self.itercount= 0
        tkn_escaped = False
        if (tkn[0] == "'" and tkn[-1] == "'") or (tkn[0] == "\"" and tkn[-1] == "\""):
            tkn_escaped = True
            tkn = tkn.strip("'\"")
        (self.operation, self.itercount) = get_operation_lambda(tkn, tkn_escaped)
        assert_with_data(self.operation, tkn, "Unknown operation")
        print_debug("Registed operation", str(self.operation), "for token", tkn)


def parse_commands(tokenstr):
    command_list = []
    print_debug("received command string:", tokenstr)
    if tokenstr[0] == ".":
        print_debug("Removing starting .")
        tokenstr=tokenstr[1:]
    idx = 0
    buffer = ""
    while idx < len(tokenstr):
        if tokenstr[idx] == ".":
            command_list.append(OperationToken(buffer))
            buffer = ""
        elif tokenstr[idx] in q_chars:
            eidx = skip_quotes(tokenstr,idx)
            buffer += tokenstr[idx:eidx+1]
            idx = eidx
        elif tokenstr[idx] == "(":
            eidx = match_bracket(tokenstr,idx)
            buffer+=tokenstr[idx:eidx+1]
            idx = eidx
        else:
            buffer += tokenstr[idx]
        idx += 1
    if buffer:
        command_list.append(OperationToken(buffer))
    return command_list


def iteration_wrapper(data, level, operation):
    if level == 0:
        print_debug(f"Applying {operation}")
        return operation(data)
    print_debug(f"Applying iterative {operation} at depth {level}")
    if isinstance(data, list):
        return [iteration_wrapper(element, level-1, operation) for element in data]
    elif isinstance(data, dict):
        newdict = {}
        for key in data:
            result = iteration_wrapper({key: data[key]}, level-1, operation)
            if result:
                if not isinstance(result, dict):
                    raise_error(
                        result, "Iteratitve operation on a json must return individual jsons")
                newdict.update(result)
        return newdict
    else:
        raise_error(data, "Cant apply iterator on list or string")


def runprogram(jsondata, parsestr):
    operations = parse_commands(parsestr)
    subval = jsondata
    while operations:
        next_task = operations.pop(0)
        print_debug(f"Token: {next_task.token}, ", end = "")
        subval = iteration_wrapper(subval, next_task.itercount, next_task.operation)
    return subval
