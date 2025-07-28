import ipaddress
from ipx.utils import analyze_ip


def test_ipv4_analysis():
    net = ipaddress.ip_network("192.168.1.0/24")
    result = analyze_ip(net)
    assert result["network_address"] == "192.168.1.0"
    assert result["broadcast_address"] == "192.168.1.255"
    assert result["netmask"] == "255.255.255.0"
    assert result["cidr"] == "192.168.1.0/24"
    assert result["usable_hosts"] == 254
    assert result["ip_version"] == 4
    assert result["is_private"] is True
    assert result["host_range"] == ["192.168.1.1", "192.168.1.254"]


def test_ipv6_analysis():
    net = ipaddress.ip_network("2001:db8::/126")
    result = analyze_ip(net)
    assert result["network_address"] == "2001:db8::"
    assert result["broadcast_address"] == "N/A"
    assert result["ip_version"] == 6
    assert result["is_private"] is False
    assert result["host_range"][0].startswith("2001:db8::")


def test_invalid_ipv4_host_range():
    net = ipaddress.ip_network("192.168.0.0/31")
    result = analyze_ip(net)
    assert result["usable_hosts"] == 0
    assert result["host_range"] == ["N/A", "N/A"]


def test_loopback():
    net = ipaddress.ip_network("127.0.0.1/8")
    result = analyze_ip(net)
    assert result["is_loopback"] is True# tests/test_main.py

import ipaddress
from ipx.utils import analyze_ip


def test_ipv4_analysis():
    net = ipaddress.ip_network("192.168.1.0/24")
    result = analyze_ip(net)
    assert result["network_address"] == "192.168.1.0"
    assert result["broadcast_address"] == "192.168.1.255"
    assert result["netmask"] == "255.255.255.0"
    assert result["cidr"] == "192.168.1.0/24"
    assert result["usable_hosts"] == 254
    assert result["ip_version"] == 4
    assert result["is_private"] is True
    assert result["host_range"] == ["192.168.1.1", "192.168.1.254"]


def test_ipv6_analysis():
    net = ipaddress.ip_network("2001:db8::/126")
    result = analyze_ip(net)
    assert result["network_address"] == "2001:db8::"
    assert result["broadcast_address"] == "N/A"
    assert result["ip_version"] == 6
    assert result["is_private"] is False
    assert result["host_range"][0].startswith("2001:db8::")


def test_invalid_ipv4_host_range():
    net = ipaddress.ip_network("192.168.0.0/31")
    result = analyze_ip(net)
    assert result["usable_hosts"] == 0
    assert result["host_range"] == ["N/A", "N/A"]


def test_loopback():
    net = ipaddress.ip_network("127.0.0.1/8")
    result = analyze_ip(net)
    assert result["is_loopback"] is True
