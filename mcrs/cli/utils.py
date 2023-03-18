import importlib
from typing import Any


def dynamic_import(name: str) -> Any:
    components = name.split(".")
    variable = components[-1]
    mod = importlib.import_module(".".join(components[:-1]))
    return getattr(mod, variable)
