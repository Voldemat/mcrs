import importlib
import os
import sys
from typing import Any


def dynamic_import(name: str) -> Any:
    working_directory = os.environ["PWD"]
    if working_directory not in sys.path:
        sys.path.insert(1, working_directory)
    module_path, variable_name = name.split(":")
    mod = importlib.import_module(module_path)
    return getattr(mod, variable_name)
