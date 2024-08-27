import os

import pytest

from mcrs import (
    EnvConfValue,
    EnvironmentConfig,
    EnvironmentManager,
)


def test_environment_config() -> None:
    class APIConfig(EnvironmentConfig):
        jwt_public_key: EnvConfValue[str] = EnvConfValue("JWT_PUBLIC_KEY")

    os.environ["JWT_PUBLIC_KEY"] = "something"
    environment = EnvironmentManager.load()
    config = APIConfig(environment)

    assert config.jwt_public_key.value == "something"


def test_environment_config_with_allow_undefined() -> None:
    class APIConfig(EnvironmentConfig):
        jwt_public_key: EnvConfValue[str] = EnvConfValue("JWT_PUBLIC_KEY")

    environment = EnvironmentManager({})
    config = APIConfig(environment, allow_undefined=True)

    assert config.jwt_public_key.value is None


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
        root_path: EnvConfValue[str] = EnvConfValue("ROOT_PATH", default="")

    if "PORT" in os.environ:
        del os.environ["PORT"]
    environment = EnvironmentManager.load()
    config = APIConfig(environment)
    assert config.port.value == 3000
    assert config.root_path.value == ""


def test_environment_config_with_nested() -> None:
    class JWTConfig(EnvironmentConfig):
        public_key: EnvConfValue[str] = EnvConfValue("JWT_PUBLIC_KEY")

    class APIConfig(EnvironmentConfig):
        jwt: JWTConfig

    os.environ["JWT_PUBLIC_KEY"] = "test_value"
    environment = EnvironmentManager.load()
    config = APIConfig(environment)
    assert config.jwt.public_key.value == "test_value"


def test_environment_config_get_variables() -> None:
    class JWTConfig(EnvironmentConfig):
        public_key: EnvConfValue[str] = EnvConfValue("JWT_PUBLIC_KEY")

    class APIConfig(EnvironmentConfig):
        jwt: JWTConfig
        host: EnvConfValue[str] = EnvConfValue("HOST")

    os.environ["JWT_PUBLIC_KEY"] = "test_value"
    os.environ["HOST"] = "test_host"
    variables = APIConfig.get_all_variables()
    assert len(variables) == 2
    assert variables[0].key == "HOST"
    assert variables[1].key == "JWT_PUBLIC_KEY"


def test_environment_config_inheritance() -> None:
    class FirstConfig(EnvironmentConfig):
        a: EnvConfValue[str] = EnvConfValue("A")

    class SecondConfig(FirstConfig):
        b: EnvConfValue[str] = EnvConfValue("B")

    os.environ["A"] = "test_value"
    os.environ["B"] = "test_host"
    variables = SecondConfig.get_all_variables()
    assert len(variables) == 2
    assert variables[0].key == "B"
    assert variables[1].key == "A"
