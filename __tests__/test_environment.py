import pytest

from mcrs import EnvironmentManager


def test_environment_get_values() -> None:
    environment = EnvironmentManager({"a": "1", "2": "211"})
    assert environment.get("a").resolve() == "1"
    assert environment.get("2").resolve() == "211"
    assert (
        environment.get("c").default("default_value").resolve()
        == "default_value"
    )
    assert environment.get("c").optional().resolve() is None
    with pytest.raises(EnvironmentManager.exc.NoValueException):
        environment.get("c").resolve()


def test_environment_convert_values() -> None:
    environment = EnvironmentManager(
        {"a": "1", "b": "2.3", "c": "1+2j", "d": "1,2,3,4"}
    )
    assert environment.get("a").converter(int).resolve() == 1
    assert environment.get("b").converter(float).resolve() == 2.3
    assert environment.get("c").converter(complex).resolve() == complex(
        real=1, imag=2
    )
    assert environment.get("d").converter(
        lambda v: list(map(int, v.split(",")))
    ).resolve() == [1, 2, 3, 4]

    assert environment.get("e").optional().converter(int).resolve() is None


def test_environment_validate_values() -> None:
    environment = EnvironmentManager(
        {"hosts": "localhost:8001,localhost:8002", "invalid_hosts": ""}
    )

    def validate_hosts(value: str) -> None:
        hosts = list(filter(lambda v: len(v) != 0, value.split(",")))
        if len(hosts) == 0:
            raise ValueError("Hosts must contain at least one host")

    assert (
        environment.get("hosts").validator(validate_hosts).resolve()
        == "localhost:8001,localhost:8002"
    )
    with pytest.raises(ValueError) as error_info:
        environment.get("invalid_hosts").validator(validate_hosts).resolve()

    assert str(error_info.value) == "Hosts must contain at least one host"


def test_environment_raise_when_trying_change_internal_mapping() -> None:
    environment = EnvironmentManager({"a": "1"})
    with pytest.raises(AttributeError) as error:
        environment._mapping["a"] = "2"
    assert str(error.value) == "Setting item is prohibited", error.value


def test_environment_raise_when_trying_set_the_internal_mapping() -> None:
    environment = EnvironmentManager(
        {
            "hello": "world",
            "someone": "1",
        }
    )
    with pytest.raises(AttributeError) as error:
        environment._mapping = {"asdsad": "12321"}  # type: ignore
    assert str(error.value) == "_mapping is readonly attribute", error.value
