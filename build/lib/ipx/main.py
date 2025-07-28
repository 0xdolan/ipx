# ipx/main.py

import ipaddress
import json
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.json import JSON
from rich.text import Text

from .utils import analyze_ip

app = typer.Typer(help="""
IPX - Modern IP subnet calculator for cybersecurity professionals.

📌 Examples:

  ▸ Analyze a single subnet:
      ipx calc 192.168.1.0/24

  ▸ Get JSON output:
      ipx calc 10.0.0.0/8 --json

  ▸ Export results to a file:
      ipx calc 192.168.0.0/24 --export result.json

  ▸ Bulk process multiple subnets from a file:
      ipx bulk cidrs.txt --export bulk.json
""")

console = Console()


def binary_breakdown(network: ipaddress._BaseNetwork) -> dict:
    bitstring = bin(int(network.network_address))[2:].zfill(network.max_prefixlen)
    groups = [bitstring[i:i + 8] for i in range(0, len(bitstring), 8)]
    return {
        "bitstring": bitstring,
        "formatted": " | ".join(groups),
        "network_bits": network.prefixlen,
        "host_bits": network.max_prefixlen - network.prefixlen,
        "groups": groups,
    }


def display_table(results: dict):
    table = Table(title=f"IP Calculation for [green]{results['input']}[/green]", box=None)
    table.add_column("Property", style="bold cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    for key, value in results.items():
        if key in ["input", "binary"]:
            continue
        if isinstance(value, list):
            value = ", ".join(value)
        table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)

    if "binary" in results:
        b = results["binary"]
        styled_parts = []
        for i, part in enumerate(b["groups"]):
            if i < b["network_bits"] // 8:
                styled_parts.append(f"[green]{part}[/green]")
            else:
                styled_parts.append(f"[dim]{part}[/dim]")
        binary_str = " [bold]|[/bold] ".join(styled_parts)
        legend = "[green]Network bits[/green], [dim]Host bits[/dim]"
        breakdown = f"{binary_str}\n{legend}"
        console.print(Panel(Text.from_markup(breakdown), title="Binary Breakdown", expand=False))


def export_to_file(data: dict, export_path: Path):
    export_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(Panel.fit(f"[bold green]Exported to:[/bold green] {export_path}"))


@app.command()
def calc(
    cidr: str = typer.Argument(..., help="IP address in CIDR format (e.g., 192.168.0.0/24)"),
    json_output: bool = typer.Option(False, "--json", help="Show raw JSON output"),
    export: Optional[Path] = typer.Option(None, "--export", help="Export output to a JSON file")
):
    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except ValueError as e:
        console.print(f"[bold red]Invalid CIDR input:[/bold red] {e}")
        raise typer.Exit(code=1)

    results = analyze_ip(net)
    results["input"] = cidr
    results["binary"] = binary_breakdown(net)

    if json_output:
        console.print(JSON.from_data(results))
    else:
        display_table(results)

    if export:
        export_to_file(results, export)


@app.command(help="Analyze multiple CIDRs from file. Example: ipx bulk cidrs.txt --export result.json")
def bulk(
    file: Path = typer.Argument(..., help="File containing one CIDR per line"),
    export: Optional[Path] = typer.Option(None, "--export", help="Export combined JSON output")
):
    if not file.exists():
        console.print(f"[bold red]File not found:[/bold red] {file}")
        raise typer.Exit(code=1)

    output = {}
    for line in file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            net = ipaddress.ip_network(line, strict=False)
            result = analyze_ip(net)
            result["input"] = line
            result["binary"] = binary_breakdown(net)
            output[line] = result
        except ValueError as e:
            output[line] = {"error": str(e)}

    console.print(JSON.from_data(output))

    if export:
        export_to_file(output, export)


if __name__ == "__main__":
    app()

