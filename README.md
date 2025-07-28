# 📦 ipx

**Modern IP subnet calculator for cybersecurity professionals.**

`ipx` is a CLI tool built in Python using [Typer](https://typer.tiangolo.com/) and [Rich](https://rich.readthedocs.io/) for beautiful terminal output. It allows you to analyze single or multiple subnets, generate JSON output, export results, and identify IP classifications like private, reserved, multicast, and more.

---

## 🚀 Features

- ✅ IPv4 & IPv6 support
- 📊 Rich table or JSON output
- 💾 Export results to file
- 📂 Bulk analysis via input file
- 🔐 Useful for cybersecurity: classify public/private/bogon/multicast/etc.

---

## 📥 Installation

### With [uv](https://github.com/astral-sh/uv):

```bash
uv pip install -e .
```

This installs `ipx` in editable mode so your changes apply immediately.

---

## 🧪 Usage

Run:

```bash
ipx --help
```

You'll see:

```
Usage: ipx [OPTIONS] COMMAND [ARGS]...

IPX - Modern IP subnet calculator for cybersecurity professionals.

📌 Examples:
▸ Analyze a single subnet:       ipx calc 192.168.1.0/24
▸ Get JSON output:               ipx calc 10.0.0.0/8 --json
▸ Export results to a file:      ipx calc 192.168.0.0/24 --export result.json
▸ Bulk process multiple subnets from a file:  ipx bulk cidrs.txt --export bulk.json

Options:
  --install-completion     Install completion for the current shell.
  --show-completion        Show completion for the current shell, to copy it or customize the installation.
  --help                   Show this message and exit.

Commands:
  calc
  bulk   Analyze multiple CIDRs from file. Example: ipx bulk cidrs.txt --export result.json

```

---

## 🔹 Command: `ipx calc`

Analyze a single CIDR subnet.

### Example:

```bash
ipx calc 192.168.0.0/24
```

### Options:

- `--json`: Output as structured JSON
- `--export PATH`: Save results to a `.json` file

### Output Example:

```
IP Calculation for 192.168.0.0/24
────────────────────────────────────────────
Property            Value
────────────────────────────────────────────
Network Address     192.168.0.0
Broadcast Address   192.168.0.255
Netmask             255.255.255.0
Wildcard Mask       0.0.0.255
CIDR                192.168.0.0/24
Usable Hosts        254
IP Version          4
Is Private          True
Is Global           False
Is Reserved         False
Is Multicast        False
Is Loopback         False
Number of Addresses 256
Host Range          192.168.0.1 - 192.168.0.254
```

---

## 🔹 Command: `ipx bulk`

Analyze multiple CIDRs from a text file.

### Example `cidrs.txt`:

```
192.168.1.0/24
10.0.0.0/8
2001:db8::/126
invalid-cidr
```

### Run:

```bash
ipx bulk cidrs.txt
```

### Options:

- `--export PATH`: Save all results as JSON

### Output:

If any CIDR is invalid, the tool will include the error:

```json
{
  "192.168.1.0/24": { ... },
  "invalid-cidr": {
    "error": "Expected 4 octets in 'invalid-cidr'"
  }
}
```

---

## 📘 Field Explanations (per subnet)

| Field               | Meaning                                                                 |
| ------------------- | ----------------------------------------------------------------------- |
| `network_address`   | First address in the subnet (not usable host)                           |
| `broadcast_address` | Last address in IPv4 (for message broadcast)                            |
| `netmask`           | Traditional mask like `255.255.255.0` or IPv6 equivalent                |
| `wildcard_mask`     | Inverse of netmask (e.g., `0.0.0.255`, `::3` for IPv6)                  |
| `cidr`              | Subnet as CIDR notation (e.g., `192.168.0.0/24`, `2001:db8::/126`)      |
| `usable_hosts`      | Hosts you can assign (usually 0 for `/31`, `/32`, or small IPv6 blocks) |
| `ip_version`        | 4 or 6                                                                  |
| `is_private`        | RFC1918 or unique local address (ULA for IPv6)                          |
| `is_global`         | Publicly routable on the internet                                       |
| `is_reserved`       | Reserved for future use or special purposes                             |
| `is_multicast`      | Used for one-to-many IPv4/IPv6 communication                            |
| `is_loopback`       | Local-only address like `127.0.0.1` or `::1`                            |
| `num_addresses`     | Total count of IPs in the range                                         |
| `host_range`        | Usable host IPs (first-last or listed range for small IPv6 subnets)     |
| `binary`            | Binary breakdown of the IP and mask, showing network and host bits      |

---

## 🧪 Testing

```bash
uv add pytest
pytest
```

---

## 🛠 Dev Workflow

```bash
uv pip install -e .
# Make changes
ipx calc 10.0.0.0/8
```

---

## 📝 License

This project is licensed under the [GNU General Public License v3.0](LICENSE).  
You are free to use, modify, and distribute this software under the terms of the GPLv3.

---

## 👤 Author

Built with ❤️ by [Dolan](https://github.com/0xdolan)
