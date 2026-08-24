import click
from .scanner import scan_network, PortScanner
from .bandwidth_monitor import live_monitor
from .packet_analyzer import PacketAnalyzer
from .topology import TopologyMapper
from rich.console import Console

console = Console()

@click.group()
def cli():
    """NetScope - Network Monitoring & Packet Analysis Tool"""
    pass

@cli.command()
@click.argument('subnet')
def scan(subnet):
    """Scan a network subnet for active hosts."""
    scan_network(subnet)

@cli.command()
@click.argument('target')
def portscan(target):
    """Scan common ports on a target host."""
    scanner = PortScanner(target)
    with console.status(f"[bold green]Scanning {target}..."):
        open_ports = scanner.scan()
    
    if open_ports:
        console.print(f"[bold green]Open ports on {target}:[/bold green] {open_ports}")
    else:
        console.print(f"[bold red]No open common ports found on {target}.[/bold red]")

@cli.command()
def monitor():
    """Real-time bandwidth monitoring."""
    try:
        live_monitor()
    except KeyboardInterrupt:
        console.print("
[bold red]Monitoring stopped.[/bold red]")

@cli.command()
@click.option('--interface', '-i', default='eth0', help='Network interface to capture on')
@click.option('--count', '-c', default=100, help='Number of packets to capture')
def capture(interface, count):
    """Capture and analyze network packets."""
    analyzer = PacketAnalyzer()
    with console.status(f"[bold blue]Capturing {count} packets on {interface}..."):
        analyzer.capture_packets(interface=interface, count=count)
    
    console.print(f"Protocols detected: {analyzer.analyze_protocols()}")
    anomalies = analyzer.detect_anomalies()
    if anomalies:
        for anomaly in anomalies:
            console.print(f"[bold red]{anomaly}[/bold red]")

@cli.command()
@click.argument('subnet')
def topology(subnet):
    """Discover network topology and export to JSON."""
    mapper = TopologyMapper()
    with console.status(f"[bold yellow]Discovering topology for {subnet}..."):
        mapper.discover_neighbors(subnet)
        mapper.export_json("topology.json")
    console.print("[bold green]Topology exported to topology.json[/bold green]")

if __name__ == '__main__':
    cli()
