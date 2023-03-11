from abc import ABC, abstractmethod

from .no_value import NoValue


class IEnvironmentManager(ABC):
    @abstractmethod
    def _get(self, key: str) -> str | NoValue:
        raise NotImplementedError
