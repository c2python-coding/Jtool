import sys
import json

# TODO make this better

def shortstr(data_dict, truncate=50):
    return json.dumps(data_dict, separators=(',', ':'))[:truncate]+"..."


def assert_with_data(condition, data, message):
    if not condition:
        if isinstance(data, list) or isinstance(data, dict):
            data = shortstr(data)
        print("Error:", message, "  (Recieved input =", str(data), ")")
        sys.exit(1)


def raise_error(data, message):
    assert_with_data(False, data, message)
