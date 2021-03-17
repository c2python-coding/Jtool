import importlib
from os import listdir
from os.path import dirname

_corepath = dirname(__file__)
_potential_modules = listdir(_corepath)
for _item in _potential_modules:
    _file = _item.rstrip(".py")
    if _file != "__init__":
        importlib.import_module("."+_file, __package__)
