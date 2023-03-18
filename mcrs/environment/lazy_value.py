from __future__ import annotations

from typing import Any, Callable

from .exceptions import DupOperationException, NoValueException


class LazyValue:
    key: str
    loader: Callable[[], str | None]
    is_optional: bool
    default_value: str | None
    converter_func: Callable[[str], Any] | None
    validator_func: Callable[[str], None] | None

    def __init__(self, key: str, loader: Callable[[], str | None]) -> None:
        self.key = key
        self.loader = loader
        self.is_optional = False
        self.default_value = None
        self.converter_func = None
        self.validator_func = None

    def default(self, value: str) -> LazyValue:
        if self.default_value is not None:
            raise DupOperationException("Default value already defined")
        self.default_value = value
        return self

    def converter(self, func: Callable[[str], Any]) -> LazyValue:
        if self.converter_func is not None:
            raise DupOperationException("Converter already defined")
        self.converter_func = func
        return self

    def optional(self) -> LazyValue:
        if self.is_optional is True:
            raise DupOperationException("Value already optional")
        self.is_optional = True
        return self

    def validator(self, validator_func: Callable[[str], None]) -> LazyValue:
        if self.validator_func is not None:
            raise DupOperationException("Validator already defined")
        self.validator_func = validator_func
        return self

    def resolve(self) -> Any:
        value = self.get_raw_value()
        if value is None:
            return None

        if self.validator_func is not None:
            self.validator_func(value)

        if self.converter_func is not None:
            return self.converter_func(value)
        return value

    def get_raw_value(self) -> str | None:
        value = self.loader()
        if value is None:
            value = self.default_value
        if value is None and not self.is_optional:
            raise NoValueException(f"Value for key {self.key} does not exists")
        return value
