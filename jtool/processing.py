
from .commandregistry import get_operation_lambda, ITER_OPERATOR
from .utils import raise_error, print_debug, assert_with_data


class OperationToken:

    def __init__(self, tkn):
        self.token = tkn
        tkn_escaped = False
        if (tkn[0] == "'" and tkn[-1] == "'") or (tkn[0] == "\"" and tkn[-1] == "\""):
            tkn_escaped = True
            tkn = tkn.strip("'\"")
        (self.operation, self.isiter) = get_operation_lambda(tkn, tkn_escaped)
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
                if tokenstr[idx] in ["'", "\""]:
                    groupchar = tokenstr[idx]
                elif tokenstr[idx] == "(":
                    groupchar = ")"
                buffer += tokenstr[idx]
        idx += 1
    assert not groupchar, f"mismatch quotes/parenthesis {groupchar}"
    if buffer:
        command_list.append(OperationToken(buffer))
    return command_list


def selectfrom(jsondata, parsestr):
    operations = parse_commands(parsestr)
    subval = jsondata
    while operations:
        next_task = operations.pop(0)
        if next_task.isiter:
            print_debug("Applying iterative operation:",
                        next_task.token, next_task.operation)
            if isinstance(subval, list):
                subval = [next_task.operation(element) for element in subval]
                subval = [element for element in subval if element is not None]
            elif isinstance(subval, dict):
                newdict = {}
                for key in subval:
                    result = next_task.operation({key: subval[key]})
                    if result:
                        if not isinstance(result, dict):
                            raise_error(result, "Iteratitve operation on a json must return invidiual jsons")
                        newdict.update(result)
                subval = newdict
            else:
                raise_error(subval, "Cant apply iterator on list or string")
        else:
            print_debug("Applying operation:",
                        next_task.token, next_task.operation)
            subval = next_task.operation(subval)
    return subval
