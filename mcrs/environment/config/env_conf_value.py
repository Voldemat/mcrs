from __future__ import annotations

from typing import (
    Any,
    Callable,
    Generic,
    Literal,
    TypeVar,
    overload,
)

from ..imanager import IEnvironmentManager


T = TypeVar("T")


class EnvConfValue(Generic[T]):
    key: str
    optional: bool
    default: str | None
    _loaded: bool
    _value: T | None
    validator: Callable[[str], None] | None
    converter: Callable[[str], Any] | None

    @overload
    def __init__(
        self: EnvConfValue[str],
        key: str,
        default: str | None = None,
        optional: Literal[False] = False,
        validator: Callable[[str], None] | None = None,
        converter: Callable[[str], str] | None = None,
    ) -> None:
        pass

    @overload
    def __init__(
        self: EnvConfValue[str | None],
        key: str,
        default: None = None,
        optional: Literal[True] = True,
        validator: Callable[[str], None] | None = None,
        converter: Callable[[str], str | None] | None = None,
    ) -> None:
        pass

    @overload
    def __init__(
        self: EnvConfValue[T],
        key: str,
        default: str | None = None,
        optional: Literal[False] = False,
        validator: Callable[[str], None] | None = None,
        converter: Callable[[str], T] | None = None,
    ) -> None:
        pass

    @overload
    def __init__(
        self: EnvConfValue[T | None],
        key: str,
        default: None = None,
        optional: Literal[True] = True,
        validator: Callable[[str], None] | None = None,
        converter: Callable[[str], T] | None = None,
    ) -> None:
        pass

    def __init__(
        self: EnvConfValue[T | str | None],
        key: str,
        default: str | None = None,
        optional: bool = False,
        validator: Callable[[str], None] | None = None,
        converter: Callable[[str], T | str | None] | None = None,
    ) -> None:
        self.key = key
        self.default = default
        self.optional = optional
        self.validator = validator
        self.converter = converter
        self._loaded = False
        self._value = None

    def load_value(
        self, environment: IEnvironmentManager, allow_undefined: bool
    ) -> None:
        loader = environment.get(self.key)
        if self.optional is True or allow_undefined is True:
            loader.optional()
        if self.validator is not None:
            loader.validator(self.validator)
        if self.converter is not None:
            loader.converter(self.converter)
        if self.default is not None:
            loader.default(self.default)
        self._value = loader.resolve()
        self._loaded = True

    @property
    def value(self) -> T:
        if not self._loaded:
            raise ValueError(f'EnvConfValue "{self.key}" not loaded value yet')
        return self._value  # type: ignore [return-value]
