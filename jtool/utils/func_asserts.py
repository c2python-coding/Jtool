from .errorhandling import raise_error
from .constants import canoncial_type_names


def lambda_type(data, *test_types):
    for t in test_types:
        if isinstance(data, t):
            return data
    raise_error(data, "selection is not of types [" + ",".join(
        canoncial_type_names[x] for x in test_types) + "]")


def lambda_member(item, collection):
    if item in collection:
        return item
    e_message = str(item) + " not in " + canoncial_type_names[type(collection)]
    raise_error(collection, e_message)


def exception_wrapper(lambdafun, data, tkn):
    try:
        val = lambdafun(data)
        return val
    except Exception as e:
        raise_error(data, "@"+ tkn+ " "+str(e))


def lambda_in_range(item, index):
    if index >= 0 and index <= len(item):
        return index
    raise_error(item, f"Index  out of range: {index}")
