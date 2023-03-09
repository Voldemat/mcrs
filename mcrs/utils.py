import resource


def get_resource_limit(n: int) -> tuple[int | None, int | None]:
    r = resource.getrlimit(n)
    return (
        r[0] if r[0] != resource.RLIM_INFINITY else None,
        r[1] if r[1] != resource.RLIM_INFINITY else None,
    )


def parse_dns_servers_from_file(
    filename: str = "/etc/resolv.conf",
) -> list[str]:
    with open(filename, "r") as file:
        return list(
            map(
                # Line example "nameserver 192.168.1.1"
                lambda line: line.replace("nameserver ", ""),
                filter(
                    lambda line: line.startswith("nameserver"),
                    file.read().splitlines(),
                ),
            )
        )
