from __future__ import annotations

import socket
from dataclasses import dataclass

from .utils import parse_dns_servers_from_file


@dataclass(frozen=True)
class Network:
    hostname: str | None
    dns_servers: list[str]
    ip_addresses: list[str]
    alternative_hostnames: list[str]
    default_socket_timeout: float | None
    network_interfaces: list[tuple[int, str]]

    @classmethod
    def load(cls) -> Network:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        alternative_hostnames: list[str] = []
        list_of_ips: list[str] = []
        try:
            (
                _,
                alternative_hostnames,
                list_of_ips,
            ) = socket.gethostbyaddr(ip_address)
        except socket.herror:
            pass
        network_interfaces = socket.if_nameindex()
        dns_servers = parse_dns_servers_from_file()
        return cls(
            hostname=hostname,
            alternative_hostnames=alternative_hostnames,
            ip_addresses=list_of_ips,
            network_interfaces=network_interfaces,
            dns_servers=dns_servers,
            default_socket_timeout=socket.getdefaulttimeout(),
        )
