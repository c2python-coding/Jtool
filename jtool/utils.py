import sys
import json

DEBUG_ENABLED = False


def enable_debug():
    global DEBUG_ENABLED
    DEBUG_ENABLED = True


def print_debug(*args):
    global DEBUG_ENABLED
    if DEBUG_ENABLED:
        print(*args)


def json2shortstr(data_dict, truncate=50):
    return json.dumps(data_dict, separators=(',', ':'))[:truncate]+"..."

##TODO this needs better error handling

def assert_with_data(condition, data, message):
    if not condition:
        print("Error:", message, "  (Recieved input =", str(data), ")")
        sys.exit(1)


def raise_error(data, message):
    assert_with_data(False, data, message)
