import os

import pytest

from mcrs import EnvConfValue, EnvironmentConfig, EnvironmentManager


def test_environment_config() -> None:
    class APIConfig(EnvironmentConfig):
        jwt_public_key: EnvConfValue[str] = EnvConfValue("JWT_PUBLIC_KEY")

    os.environ["JWT_PUBLIC_KEY"] = "something"
    environment = EnvironmentManager.load()
    config = APIConfig(environment)

    assert config.jwt_public_key.value == "something"


def test_environment_config_with_optional() -> None:
    class APIConfig(EnvironmentConfig):
        jwt_public_key: EnvConfValue[str | None] = EnvConfValue(
            "JWT_PUBLIC_KEY", optional=True
        )

    del os.environ["JWT_PUBLIC_KEY"]
    environment = EnvironmentManager.load()
    config = APIConfig(environment)
    assert config.jwt_public_key.value is None


def test_environment_config_with_validator() -> None:
    class CheckException(Exception):
        pass

    def validator(v: str) -> None:
        raise CheckException()

    class APIConfig(EnvironmentConfig):
        jwt_public_key: EnvConfValue[str] = EnvConfValue(
            "JWT_PUBLIC_KEY", validator=validator
        )

    os.environ["JWT_PUBLIC_KEY"] = "something"
    environment = EnvironmentManager.load()
    with pytest.raises(CheckException):
        APIConfig(environment)


def test_environment_config_with_converter() -> None:
    class APIConfig(EnvironmentConfig):
        port: EnvConfValue[int] = EnvConfValue("PORT", converter=int)

    os.environ["PORT"] = "8000"
    environment = EnvironmentManager.load()
    config = APIConfig(environment)
    assert config.port.value == 8000


def test_environment_config_with_default() -> None:
    class APIConfig(EnvironmentConfig):
        port: EnvConfValue[int] = EnvConfValue(
            "PORT", converter=int, default="3000"
        )

    if "PORT" in os.environ:
        del os.environ["PORT"]
    environment = EnvironmentManager.load()
    config = APIConfig(environment)
    assert config.port.value == 3000
