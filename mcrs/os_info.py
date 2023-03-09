from __future__ import annotations

import platform
from dataclasses import dataclass


@dataclass(frozen=True)
class OSInfo:
    system: str
    release: str
    machine: str
    version: str

    @classmethod
    def load(cls) -> OSInfo:
        return cls(
            machine=platform.machine(),
            release=platform.release(),
            system=platform.system(),
            version=platform.version(),
        )
