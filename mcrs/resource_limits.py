from __future__ import annotations

import resource
from dataclasses import dataclass

from .utils import get_resource_limit


@dataclass(frozen=True)
class Limit:
    soft: int | None
    hard: int | None


@dataclass(frozen=True)
class ResourceLimits:
    page_size: int
    max_cpu_time: Limit
    max_file_size: Limit
    max_ram_heap: Limit
    max_ram_stack: Limit
    max_open_files: Limit
    max_child_processes: Limit

    @classmethod
    def load(cls) -> ResourceLimits:
        return ResourceLimits(
            page_size=resource.getpagesize(),
            max_cpu_time=Limit(*get_resource_limit(resource.RLIMIT_CPU)),
            max_file_size=Limit(*get_resource_limit(resource.RLIMIT_FSIZE)),
            max_ram_heap=Limit(*get_resource_limit(resource.RLIMIT_DATA)),
            max_ram_stack=Limit(*get_resource_limit(resource.RLIMIT_STACK)),
            max_child_processes=Limit(
                *get_resource_limit(resource.RLIMIT_NPROC)
            ),
            max_open_files=Limit(*get_resource_limit(resource.RLIMIT_NOFILE)),
        )
