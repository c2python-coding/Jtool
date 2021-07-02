from .registry import get_operation_lambda
from jtool.utils.errorhandling import raise_error, assert_with_data
from jtool.utils.debug import print_debug


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
        print_debug("Parsed token", tkn, "for operation", str(self.operation))


def parse_commands(tokenstr):
    command_list = []
    print_debug("received command string:", tokenstr)
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
                command_list.append(OperationToken(buffer))
                buffer = ""
            else:
                # escapes the stuff in quotes as one singular entry.
                if tokenstr[idx] in ["'", "\""]:
                    groupchar = tokenstr[idx]
                elif tokenstr[idx] == "(":
                    groupchar = ")"
                buffer += tokenstr[idx]
        idx += 1
    if groupchar:
        raise_error(tokenstr, "mismatched parenthesis")
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
        print_debug(f"Next operation token: {next_task.token}")
        subval = iteration_wrapper(subval, next_task.itercount, next_task.operation)
    return subval
