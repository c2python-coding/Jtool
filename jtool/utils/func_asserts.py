from .errorhandling import raise_error
from .constants import canoncial_type_names



def lambda_type(data, ttype):
    if isinstance(data, ttype):
        return data
    raise_error(data, "selection is not of type " + canoncial_type_names[ttype])


def lambda_multi_type(data, *test_types):
    for t in test_types:
        if isinstance(data, t):
            return data
    raise_error(data, "selection is not of types [" + ",".join(canoncial_type_names[x] for x in test_types) + "]") 


def lambda_member(item, collection):
    if item in collection:
        return item
    collection_str = "collection"
    if isinstance(collection, list):
        collection_str = "list"
    if isinstance(collection, dict):
        collection_str = "dict"
    e_message = str(item) + " not in " + collection_str
    raise_error(collection, e_message)


def exception_wrapper(lambdafun, data, errormsg):
    try:
        val = lambdafun(data)
        return val
    except Exception:
        raise_error(data, errormsg)
