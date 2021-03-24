import sys
import argparse
from argparse import RawTextHelpFormatter
from . import execution
from . import operations
from .utils.debug import enable_debug


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

first_help_items = ["core operators", "parsers"]


def build_help_str(namespace):
    items = execution.registry.COMMAND_HELP_LIST[namespace]
    headerstr = "---"+" ".join(x.capitalize()
                               for x in namespace.split("_")) + "---\n"
    cmdstr = "\n".join(cmd for cmd in items)
    return "\n"+headerstr+cmdstr+"\n"


def run():
    description_str = _INITIAL_HELP_STR+"\n"
    for item in first_help_items:
        description_str += build_help_str(item)

    for namespace in execution.registry.COMMAND_HELP_LIST:
        if namespace not in first_help_items:
            description_str += build_help_str(namespace)

    parser = argparse.ArgumentParser(
        description=description_str, formatter_class=RawTextHelpFormatter)
    parser.add_argument("commandstr", help="selector command", nargs="?")
    parser.add_argument("-f", "--filename", required=False,
                        metavar='FILE', help="process file instead of stdin")
    parser.add_argument("-d", "--debug", action='store_true',
                        help="print debug trace", required=False)
    args = parser.parse_args()
    data = {}
    if (args.debug):
        enable_debug()

    # TODO make this buffered reading
    if args.filename:
        with open(args.filename, "r") as f:
            data = f.read()
    else:
        data = sys.stdin.read()
    if args.commandstr:
        parsestring = args.commandstr
        result = execution.runprogram(data, parsestring)
        if result:
            print(str(result))
    else:
        print(data)


if __name__ == "__main__":
    run()
