import sys
import re 

# TODO make this better


def assert_with_data(condition, data, message):
    if not condition:
        pdata = str(data)[:50] + ("..." if len(str(data)) > 50 else "")
        print("Error:", message, "  (Recieved input =", pdata, ")")
        sys.exit(1)


def raise_error(data, message):
    assert_with_data(False, data, message)


def validate_re(re_expression):
    try:
        re.compile(re_expression)
    except re.error as e:
        raise_error(re_expression, str(e))