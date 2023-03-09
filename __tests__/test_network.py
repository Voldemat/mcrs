import dataclasses
import socket

import pytest

from mcrs import Network, parse_dns_servers_from_file


def test_network_is_immutable() -> None:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    _, alternative_hostnames, list_of_ips = socket.gethostbyaddr(ip_address)
    network = Network(
        dns_servers=parse_dns_servers_from_file(),
        network_interfaces=socket.if_nameindex(),
        default_socket_timeout=socket.getdefaulttimeout(),
        hostname=hostname,
        alternative_hostnames=alternative_hostnames,
        ip_addresses=list_of_ips,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        network.ip_addresses = []  # type: ignore [misc]
