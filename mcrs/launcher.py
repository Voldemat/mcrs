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
            self.setup(instance, loop)
            loop.run_until_complete(instance.main())
        finally:
            self.shutdown(instance, loop)

    def setup(
        self, instance: IMicroService, loop: asyncio.AbstractEventLoop
    ) -> None:
        with DelayedInterrupt():
            loop.run_until_complete(instance.setup())

    def shutdown(
        self, instance: IMicroService, loop: asyncio.AbstractEventLoop
    ) -> None:
        with DelayedInterrupt():
            loop.run_until_complete(instance.shutdown())
            try:
                self._cancel_all_task(loop)
                loop.run_until_complete(loop.shutdown_asyncgens())
            finally:
                loop.close()

    def _cancel_all_task(self, loop: asyncio.AbstractEventLoop) -> None:
        to_cancel = asyncio.tasks.all_tasks(loop)
        if not to_cancel:
            return

        for task in to_cancel:
            task.cancel()

        loop.run_until_complete(
            asyncio.tasks.gather(*to_cancel, return_exceptions=True)
        )

        for task in filter(lambda task: not task.cancelled(), to_cancel):
            if task_exc := task.exception():
                loop.call_exception_handler(
                    {
                        "message": "unhandled exception during shutdown",
                        "exception": task_exc,
                        "task": task,
                    }
                )
