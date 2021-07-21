# Jtool

A tool for processing json/html/xml/csv/text data with json like manipulation. 

Aimed for easy use and extensibilty. 

## Requirements

Developed for `python3.6+`, not guaranteed to work on older versions

## Usage

You can clone the directory and install the tool in editable mode with 

```sh
pip install -e Jtool
```

You can then see the options using the `jtool -h ` flag

```txt
usage: jtool [-h] [-f FILE] [-d] [commandstr]

A tool for working with json/csv/xml/html/text data

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
See `-h` for a list of available commands


## Custom commands

All commands are defined in files in the `operations` folder and allow for extending the query language. 
Each command must follow the following specification:

### 1. Commands
The commands name  name (ex. `moo`) is referenced as follows in the query string.
*  `@moo` for a non parameter command or
*  `@moo(...)` for a parameter command where `...` is a string with whatever parameters are in the query string. 

The parameter string in the paretheses is automatically escaped, so using , core operators or other `@` commands does not cause errors

### 2. Registration
To add the command `moo`, define a new function using the following format 

```python
@register_command("moo")  # required to register command
def make_KEYS_op(params): # function name not imporant
    '''description, as displayed when jtool -h is invoked'''
    #params is optional and will be a string that is between () in the command spec
    #the processing code here must define a callable (lambda or function)
    #that takes a valid input  and returns something
    return lambda data: {"mooable":data}

```

The returning callable will be invoked in the chain of operations specified by the query string when encountered. 
The data passed to the callable will be the current selection up to that operation. It is up to you to ensure that your custom
operation plays nicely with others. 

Happy usage!
