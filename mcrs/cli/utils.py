import importlib
import os
import sys
from typing import Any


def dynamic_import(name: str) -> Any:
    working_directory = os.environ["PWD"]
    if working_directory not in sys.path:
        sys.path.insert(1, working_directory)
    components = name.split(".")
    variable = components[-1]
    mod = importlib.import_module(".".join(components[:-1]))
    return getattr(mod, variable)
