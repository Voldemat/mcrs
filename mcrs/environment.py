from __future__ import annotations

import os
from typing import Any, TypeVar, overload


T = TypeVar("T")
KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")


class ImmutableMapping(dict[KeyType, ValueType]):
    _init: bool = False

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._init = True

    def __setitem__(self, *args: Any, **kwargs: Any) -> None:
        if self._init:
            raise AttributeError("Couldn`t change ImmutableMapping")
        return super().__setattr__(*args, **kwargs)

    def __delitem__(self, *args: Any, **kwargs: Any) -> None:
        raise AttributeError("Couldn`t change ImmutableMapping")


class Environment:
    _mapping: ImmutableMapping[str, str]
    _init: bool = False

    def __init__(self, mapping: dict[str, str]) -> None:
        self._mapping = ImmutableMapping(mapping)
        self._init = True

    @property
    def mapping(self) -> ImmutableMapping[str, str]:
        return self._mapping

    @overload
    def get(self, key: str, default: None = None) -> str | None:
        pass

    @overload
    def get(self, key: str, default: T) -> str | T:
        pass

    def get(self, key: str, default: T | None = None) -> str | T | None:
        return self._mapping.get(key, default)

    def __setattr__(self, key: str, value: Any) -> None:
        if key == "_mapping" and self._init:
            raise AttributeError("_mapping is readonly attribute")
        return super().__setattr__(key, value)

    def __delattr__(self, key: str) -> None:
        if key == "_mapping":
            raise AttributeError("_mapping is readonly attribute")
        return super().__delattr__(key)

    @classmethod
    def load(cls) -> Environment:
        return cls(dict(os.environ))
