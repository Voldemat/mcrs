from __future__ import annotations

import inspect
from typing import Any, Iterable, Type

from .env_conf_value import EnvConfValue
from ..imanager import IEnvironmentManager


class EnvironmentConfig:
    def __init__(
        self, environment: IEnvironmentManager, allow_undefined: bool = False
    ) -> None:
        self.allow_undefined = allow_undefined
        self.load_values(environment)
        self.load_configs(environment)

    def load_values(self, environment: IEnvironmentManager) -> None:
        for value in self.get_env_values():
            value.load_value(environment, allow_undefined=self.allow_undefined)

    def load_configs(self, environment: IEnvironmentManager) -> None:
        for key, ConfigClass in self.get_configs():
            setattr(
                self,
                key,
                ConfigClass(environment, allow_undefined=self.allow_undefined),
            )

    @classmethod
    def get_env_values(cls) -> Iterable[EnvConfValue[Any]]:
        return filter(
            lambda value: isinstance(value, EnvConfValue),
            cls.__dict__.values(),
        )

    @classmethod
    def get_configs(cls) -> Iterable[tuple[str, Type[EnvironmentConfig]]]:
        return filter(
            lambda item: inspect.isclass(item[1])
            and issubclass(item[1], EnvironmentConfig),
            inspect.get_annotations(cls, eval_str=True).items(),
        )

    @classmethod
    def get_all_variables(cls) -> list[EnvConfValue[Any]]:
        variables = list(cls.get_env_values())
        for _, ConfigClass in cls.get_configs():
            variables += ConfigClass.get_all_variables()
        return variables
