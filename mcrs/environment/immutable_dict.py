from typing import Any, TypeVar

KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")


class ImmutableDict(dict[KeyType, ValueType]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def __setitem__(self, *args: Any, **kwargs: Any) -> None:
        raise AttributeError("Setting item is prohibited")

    def __delitem__(self, *args: Any, **kwargs: Any) -> None:
        raise AttributeError("Deleting item is prohibited")
