import re


def type_assert(data, ttype):
    if isinstance(data, ttype):
        return data
    raise AssertionError("selection is not of " + str(ttype))


def generic_assert(data, chklambda, message):
    if chklambda(data):
        return data
    raise AssertionError(message)


def membership_assert(item, collection):
    if item in collection:
        return item
    collection_str = "collection"
    if isinstance(collection, list):
        collection_str = "list"
    if isinstance(collection, dict):
        collection_str = "dict"
    raise AssertionError(str(item) + " not in " + collection_str)


def re_assert(data, regexp, message):
    if re.search(regexp, data):
        return data
    raise AssertionError(message)

