from jtool.execution.registry import register_command

@register_command("count")
def make_COUNT_op():
    '''counts number of elements in list or top level values in dict'''
    return lambda data: len(data)


@register_command("type")
def make_TYPE_op():
    '''returns type of data'''
    return lambda data: type(data).__name__ if not isinstance(data, dict) else "json"

