from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeVar

from .manager import EnvironmentManager


T = TypeVar("T")


class EnvConfValue(Generic[T]):
    key: str
    optional: bool
    default: str | None
    _loaded: bool
    _value: T | None
    validator: Callable[[str], None] | None
    converter: Callable[[str], Any] | None

    def __init__(
        self,
        key: str,
        default: str | None = None,
        optional: bool = False,
        validator: Callable[[str], None] | None = None,
        converter: Callable[[str], Any] | None = None,
    ) -> None:
        self.key = key
        self.default = default
        self.optional = optional
        self.validator = validator
        self.converter = converter
        self._loaded = False
        self._value = None

    def load_value(self, environment: EnvironmentManager) -> None:
        loader = environment.get(self.key)
        if self.optional:
            loader.optional()
        if self.validator:
            loader.validator(self.validator)
        if self.converter:
            loader.converter(self.converter)
        if self.default:
            loader.default(self.default)
        self._value = loader.resolve()
        self._loaded = True

    @property
    def value(self) -> T | None:
        if not self._loaded:
            raise ValueError(f'EnvConfValue "{self.key}" not loaded value yet')
        return self._value


class IEnvironmentConfig(ABC):
    @abstractmethod
    def __init__(self, environment: EnvironmentManager) -> None:
        raise NotImplementedError


class EnvironmentConfig(IEnvironmentConfig):
    def __init__(self, environment: EnvironmentManager) -> None:
        for value in filter(
            lambda value: isinstance(value, EnvConfValue),
            self.__class__.__dict__.values(),
        ):
            value.load_value(environment)
        for key, ConfigClass in filter(
            lambda item: inspect.isclass(item[1])
            and issubclass(item[1], IEnvironmentConfig),
            self.__class__.__annotations__.items(),
        ):
            setattr(self, key, ConfigClass(environment))
