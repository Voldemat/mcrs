from __future__ import annotations

import os
from typing import Any

from . import exceptions
from .imanager import IEnvironmentManager
from .immutable_dict import ImmutableDict
from .lazy_value import LazyValue
from .no_value import NoValue


class EnvironmentManager(IEnvironmentManager):
    exc = exceptions
    _mapping: ImmutableDict[str, str]
    _init: bool = False

    def __init__(self, mapping: dict[str, str]) -> None:
        self._mapping = ImmutableDict(mapping)
        self._init = True

    def get(self, key: str) -> LazyValue:
        return LazyValue(key, self)

    def _get(self, key: str) -> str | NoValue:
        return self._mapping.get(key, NoValue.build())

    def __setattr__(self, key: str, value: Any) -> None:
        if key == "_mapping" and self._init:
            raise AttributeError("_mapping is readonly attribute")
        if key == "_init" and self._init:
            raise AttributeError("_init is readonly attribute")
        return super().__setattr__(key, value)

    def __delattr__(self, key: str) -> None:
        if key == "_mapping":
            raise AttributeError("_mapping is readonly attribute")
        if key == "_init":
            raise AttributeError("_init is readonly attribute")
        return super().__delattr__(key)

    @classmethod
    def load(cls) -> EnvironmentManager:
        return cls(dict(os.environ))
