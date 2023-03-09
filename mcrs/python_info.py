from __future__ import annotations

import platform
from dataclasses import dataclass


@dataclass(frozen=True)
class PythonInfo:
    version: str
    build_date: str
    implementation: str

    @classmethod
    def load(cls) -> PythonInfo:
        _, build_date = platform.python_build()
        return cls(
            build_date=build_date,
            version=platform.python_version(),
            implementation=platform.python_implementation(),
        )
