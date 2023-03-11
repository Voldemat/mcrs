from abc import ABC, abstractmethod


class IEnvironmentManager(ABC):
    @abstractmethod
    def _get(self, key: str) -> str | None:
        raise NotImplementedError
