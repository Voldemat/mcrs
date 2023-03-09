import pytest

from mcrs import Environment


def test_environment_get_values() -> None:
    environment = Environment({"a": "1", "2": "211"})
    assert environment.get("a") == "1"
    assert environment.get("2") == "211"


def test_environment_raise_when_trying_change_internal_mapping() -> None:
    environment = Environment({"a": "1"})
    with pytest.raises(AttributeError) as error:
        environment._mapping["a"] = "2"
    assert str(error.value) == "Couldn`t change ImmutableMapping", error.value


def test_environment_raise_when_trying_set_the_internal_mapping() -> None:
    environment = Environment(
        {
            "hello": "world",
            "someone": "1",
        }
    )
    with pytest.raises(AttributeError) as error:
        environment._mapping = {"asdsad": "12321"}  # type: ignore
    assert str(error.value) == "_mapping is readonly attribute", error.value
