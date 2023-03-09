import asyncio
from typing import Type

from .execution_context import ExecutionContext
from .imicroservice import IMicroService
from .lifespan import DelayedInterrupt


class BaseLauncher:
    microservice: Type[IMicroService]

    def __init__(self, microservice: Type[IMicroService]) -> None:
        self.microservice = microservice

    def run(
        self, loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    ) -> None:
        instance = self.microservice(ExecutionContext.create())
        self.main(instance, loop)

    def main(
        self, instance: IMicroService, loop: asyncio.AbstractEventLoop
    ) -> None:
        try:
            with DelayedInterrupt():
                loop.run_until_complete(instance.setup())
            loop.run_until_complete(instance.main())
        finally:
            with DelayedInterrupt():
                loop.run_until_complete(instance.shutdown())
