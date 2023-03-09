import dataclasses
import platform

import pytest

from mcrs import OSInfo, PythonInfo


def test_os_info_is_immutable() -> None:
    os_info = OSInfo(
        machine=platform.machine(),
        release=platform.release(),
        system=platform.system(),
        version=platform.version(),
    )

    with pytest.raises(dataclasses.FrozenInstanceError):
        os_info.machine = "asdsad"  # type: ignore


def test_python_info_is_immutable() -> None:
    _, build_date = platform.python_build()
    python_info = PythonInfo(
        build_date=build_date,
        version=platform.python_version(),
        implementation=platform.python_implementation(),
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        python_info.version = ""  # type: ignore
