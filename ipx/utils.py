import ipaddress

def analyze_ip(net: ipaddress._BaseNetwork) -> dict:
    info = {
        "network_address": str(net.network_address),
        "broadcast_address": str(net.broadcast_address) if net.version == 4 else "N/A",
        "netmask": str(net.netmask),
        "wildcard_mask": str(net.hostmask),
        "cidr": str(net.with_prefixlen),
        "usable_hosts": (net.num_addresses - 2 if net.version == 4 and net.prefixlen < 31 else 0),
        "ip_version": net.version,
        "is_private": net.is_private,
        "is_global": net.is_global,
        "is_reserved": net.is_reserved,
        "is_multicast": net.is_multicast,
        "is_loopback": net.is_loopback,
        "num_addresses": net.num_addresses,
        "host_range": get_host_range(net)
    }
    return info


def get_host_range(net: ipaddress._BaseNetwork):
    if net.version == 4 and net.prefixlen < 31:
        first = net.network_address + 1
        last = net.broadcast_address - 1
        return [str(first), str(last)]
    elif net.version == 6 and net.prefixlen < 127:
        first = net.network_address + 1
        last = list(net.hosts())[-1]
        return [str(first), str(last)]
    else:
        return ["N/A", "N/A"]
