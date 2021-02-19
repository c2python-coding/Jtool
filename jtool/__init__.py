import sys
import json
import argparse
from argparse import RawTextHelpFormatter
from . import commandregistry
from . import customcommands
from .processing import selectfrom
from .utils import enable_debug


_INITIAL_HELP_STR = """A tool for selecting json fields. Accepts a file or stdin as input
Syntax for the selector command string follows the dot (.) notaion, where commands
are separated by period.
For special characters in selectors or expressions,  you can use single/double quotes 
to avoid interpretation as a command
The following are valid commands. Some take arguments passed in ():

"""


def run():
    description_str = _INITIAL_HELP_STR + \
        "\n".join("  "+x for x in commandregistry.COMMAND_HELP_LIST)
    parser = argparse.ArgumentParser(
        description=description_str, formatter_class=RawTextHelpFormatter)
    parser.add_argument("commandstr", help="json select command", nargs="?")
    parser.add_argument("-f", "--filename", required=False,
                        metavar='FILE', help="process file instead of stdin")
    parser.add_argument("-d", "--debug", action='store_true',
                        help="print debug trace", required=False)
    args = parser.parse_args()
    if (args.debug):
        enable_debug()
    if args.commandstr:
        parsestring = args.commandstr
        if args.filename:
            with open(args.filename, "r") as f:
                data = json.load(f)
        else:
            data = json.loads(sys.stdin.read())
        result = selectfrom(data, parsestring)
        if isinstance(result, str):
            print(result)
        else:
            print(json.dumps(result, indent=4))


if __name__ == "__main__":
    run()
