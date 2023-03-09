from mcrs import BaseLauncher, ExecutionContext, IMicroService


class CheckMicroService(IMicroService):
    def __init__(
        self,
        execution_context: ExecutionContext,
    ) -> None:
        self.context = execution_context

    async def setup(self) -> None:
        pass

    async def main(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass


def test_launcher() -> None:
    launcher = BaseLauncher(CheckMicroService)
    launcher.run()
