from click.testing import CliRunner

import pytest

from mcrs import EnvConfValue, EnvironmentConfig
from mcrs.cli import show_env


class TestConfig(EnvironmentConfig):
    __test__ = False
    host: EnvConfValue[str] = EnvConfValue("HOST")


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_cli_env(runner: CliRunner) -> None:
    result = runner.invoke(
        show_env, ["--config-module-path", "__tests__.test_cli.TestConfig"]
    )
    assert result.exit_code == 0, result.output
    assert result.output == '"HOST" required\n', result.output
