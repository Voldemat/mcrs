from abc import ABC, abstractmethod

from .execution_context import ExecutionContext


class IMicroService(ABC):
    @abstractmethod
    def __init__(self, execution_context: ExecutionContext) -> None:
        raise NotImplementedError

    @abstractmethod
    async def setup(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def main(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def shutdown(self) -> None:
        raise NotImplementedError
