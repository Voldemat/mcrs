from __future__ import annotations

import os
from typing import Any

from . import exceptions
from .imanager import IEnvironmentManager
from .immutable_dict import ImmutableDict
from .lazy_value import LazyValue


class EnvironmentManager(IEnvironmentManager):
    exc = exceptions
    _mapping: ImmutableDict[str, str]
    _init: bool = False

    def __init__(self, mapping: dict[str, str]) -> None:
        self._mapping = ImmutableDict(mapping)
        self._init = True

    def get(self, key: str) -> LazyValue:
        return LazyValue(key, lambda: self._get(key))

    def _get(self, key: str) -> str | None:
        return self._mapping.get(key)

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
