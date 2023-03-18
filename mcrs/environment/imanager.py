from abc import ABC, abstractmethod

from .lazy_value import LazyValue


class IEnvironmentManager(ABC):
    @abstractmethod
    def get(self, key: str) -> LazyValue:
        raise NotImplementedError
