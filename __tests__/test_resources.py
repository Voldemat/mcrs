import dataclasses
import resource

import pytest

from mcrs import Limit, ResourceLimits, get_resource_limit


def test_resource_limits_is_immutable() -> None:
    resource_limits = ResourceLimits(
        page_size=resource.getpagesize(),
        max_cpu_time=Limit(*get_resource_limit(resource.RLIMIT_CPU)),
        max_file_size=Limit(*get_resource_limit(resource.RLIMIT_FSIZE)),
        max_ram_heap=Limit(*get_resource_limit(resource.RLIMIT_DATA)),
        max_ram_stack=Limit(*get_resource_limit(resource.RLIMIT_STACK)),
        max_child_processes=Limit(*get_resource_limit(resource.RLIMIT_NPROC)),
        max_open_files=Limit(*get_resource_limit(resource.RLIMIT_NOFILE)),
    )

    with pytest.raises(dataclasses.FrozenInstanceError):
        resource_limits.page_size = 123123  # type: ignore
