from .errorhandling import raise_error
from .constants import canoncial_type_names


def lambda_type(data, *test_types):
    for t in test_types:
        if isinstance(data, t):
            return data
    raise_error(data, "selection is not of types [" + ",".join(canoncial_type_names[x] for x in test_types) + "]")


def lambda_member(item, collection):
    if item in collection:
        return item
    e_message = str(item) + " not in " + canoncial_type_names[type(collection)]
    raise_error(collection, e_message)


def exception_wrapper(lambdafun, data, errormsg):
    try:
        val = lambdafun(data)
        return val
    except Exception:
        raise_error(data, errormsg)
