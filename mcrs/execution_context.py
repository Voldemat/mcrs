from __future__ import annotations

from dataclasses import dataclass

from .environment import Environment
from .network import Network
from .os_info import OSInfo
from .python_info import PythonInfo
from .resource_limits import ResourceLimits


@dataclass
class ExecutionContext:
    os_info: OSInfo
    network: Network
    python_info: PythonInfo
    environment: Environment
    resource_limits: ResourceLimits

    @classmethod
    def create(cls) -> ExecutionContext:
        return cls(
            environment=Environment.load(),
            network=Network.load(),
            python_info=PythonInfo.load(),
            os_info=OSInfo.load(),
            resource_limits=ResourceLimits.load(),
        )
