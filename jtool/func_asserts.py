from .utils import raise_error, json2shortstr


def lambda_type(data, ttype):
    if isinstance(data, ttype):
        return data
    raise_error(json2shortstr(data), "selection is not of " + str(ttype))


def lambda_multi_type(data, *test_types):
    for t in test_types:
        if isinstance(data, t):
            return data
    raise_error(json2shortstr(data),
                "selection is not of " + str(t))


def lambda_member(item, collection):
    if item in collection:
        return item
    collection_str = "collection"
    if isinstance(collection, list):
        collection_str = "list"
    if isinstance(collection, dict):
        collection_str = "dict"
    e_message = str(item) + " not in " + collection_str
    raise_error(json2shortstr(collection), e_message)
