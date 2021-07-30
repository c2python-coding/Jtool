import sys
import select
import argparse
from argparse import RawTextHelpFormatter
from . import execution
from . import operations
from .utils.debug import enable_debug

"""test help"""



_INITIAL_HELP_STR = """A tool for processing json/html/xml/csv/text data.

Processing is accomplished by specifying a chain of commands separated by (.), where each
command takes the input produced by the previous command and sends the output to the next
command. For special characters in selectors or expressions, you can use single/double
quotes to avoid interpretation as a command

The input data by default is parsed as text string
The parser commands force a specific parser to be applied to data, such as json, csv, etc

The render operations cause the filtered/processed data to be rendered in the specified form.
By default, the output is a string, since it can represent all types of data.


The following are valid commands. Some take arguments passed in ().


"""


def parse(content, commandstr, debug=False):
    if (debug):
        enable_debug()
    return execution.runprogram(content, commandstr)



def _build_help_str(namespace):
    items = execution.registry.COMMAND_HELP_LIST[namespace]
    headerstr = "---"+" ".join(x for x in namespace.split("_")) + "---\n"
    cmdstr = "\n".join(cmd for cmd in items)
    return "\n"+headerstr+cmdstr+"\n"


_first_help_items = ["CORE", "PARSERS"]

_full_help_str = _INITIAL_HELP_STR+"\n"
for _item in _first_help_items:
    _full_help_str += _build_help_str(_item)

for _namespace in execution.registry.COMMAND_HELP_LIST:
    if _namespace not in _first_help_items:
        _full_help_str += _build_help_str(_namespace)

parse.__doc__=_full_help_str


def _script_entry():
    global _full_help_str
    parser = argparse.ArgumentParser(
        description=_full_help_str, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "commandstr", help="selector command", nargs="?", default='')
    parser.add_argument("-f", "--filename", required=False,
                        metavar='FILE', help="process file instead of stdin")
    parser.add_argument("-d", "--debug", action='store_true',
                        help="print debug trace", required=False)
    args = parser.parse_args()

    data = ""

    if args.filename:
        with open(args.filename, "r") as f:
            data = f.read()
    else:
        if select.select([sys.stdin,],[],[],0.0)[0]:
            data = sys.stdin.read()
        else:
            print("No stdin or --filname provided")


    if not data:
        return

    if not args.commandstr:
        print(data)
    else:
        print(parse(data, args.commandstr, args.debug))
