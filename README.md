# Jtool


JSON selection tool on par with json, aimed for easy extensibility with Python

## Requirements

Developed for python3.6+`, not guaranteed to work on older versions

## Usage

You can clone the directory and install the tool in editable mode with 

```sh
pip install -e Jtool
```

You can then see the options using the `jtool -h ` flag

```txt
usage: jtool [-h] [-f FILE] [-d] [commandstr]

A tool for selecting json fields. Accepts a file or stdin as input
Syntax for the selector command string follows the dot (.) notaion, where commands
are separated by period.
For special characters in selectors or expressions,  you can use single/double quotes 
to avoid interpretation as a command
The following are valid commands. Some take arguments passed in ():

  key : selects the particular key from the given top level json
  - : identity operator (returns the current selection without modification)
  {} : selects multiple keys from the current dictionary
  [] : selects range or particular indicies of arrays
  * : applies next command iteratively on items in a list
  @keys : returns the keys at the top level
  @keys2array : creates array from values of top level keys
  @flatten : combines list of lists into a list
  @unique : selects unique values from list
  @count : counts number of elements in list or top level values in dict
  @type : returns type of data
  @refilter : regexp filter on list based on the syntax (selector=>regular_expression)

positional arguments:
  commandstr            json select command

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --filename FILE
                        process file instead of stdin
  -d, --debug           print debug trace
```

### Query Language

The queries for the jtool are written in dot (.) notation where each command is separated by a period. 

For example, for a file test.json

```json
{
    "data": [
        {
            "akey": [
                1,
                2,
                3
            ]
        },
        {
            "akey": [
                4,
                5,
                6
            ]
        }
    ]
}
```

the command 

```sh
jtool -f test.json  "data.*.akey.*.[1]"`
```

will return 

```json
[
    2,
    5
]
```

See the `-h` for all available query 

## Custom commands

Custom commands are defined in `customcommands.py` file and allow for extending the query language. 

Each custom command must follow the following specification

### 1. Commands
The commands name  name (ex. `moo`) is referenced as follows in the query string.
*  `@moo` for a non parameter command or
*  `@moo(...)` for a parameter command where `...` is a string with whatever parameters are in the query string. 

### 2. Registration
To add the command `moo`, in the `customcommands.py` file, define a new function using the following format 

```python
@register_command("moo")  # required to register command
def make_KEYS_op(params): # function name not imporant
    '''description, as displayed when jtool -h is invoked'''
    #params will be a string that is between (), non including the ()
    parse_parameters(params)
    #the processing code here must define a callable (lambda or function)
    #that takes a valid json element 
    #and returns something
    return lambda data: {"mooable":data}

```

The returning callable will be invoked in the chain of operations specified by the query string when encountered. 
The data passed to the callable will be the current selection up to that operation. It is up to you to ensure that your custom
operation plays nicely with others. 
