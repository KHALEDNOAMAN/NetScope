import psutil
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()

class BandwidthMonitor:
    def __init__(self):
        self.last_io = psutil.net_io_counters(pernic=True)
        self.last_time = time.time()

    def get_interface_stats(self):
        current_io = psutil.net_io_counters(pernic=True)
        current_time = time.time()
        
        stats = {}
        for iface, io in current_io.items():
            if iface in self.last_io:
                dt = current_time - self.last_time
                bytes_sent = io.bytes_sent - self.last_io[iface].bytes_sent
                bytes_recv = io.bytes_recv - self.last_io[iface].bytes_recv
                
                stats[iface] = {
                    "sent_bps": (bytes_sent * 8) / dt,
                    "recv_bps": (bytes_recv * 8) / dt
                }
                
        self.last_io = current_io
        self.last_time = current_time
        return stats

    def calculate_speed(self, bps):
        mbps = bps / (1024 * 1024)
        return round(mbps, 2)

    def generate_report(self):
        stats = self.get_interface_stats()
        table = Table(title="Real-Time Bandwidth Monitor")
        table.add_column("Interface", style="cyan")
        table.add_column("Tx (Mbps)", justify="right", style="magenta")
        table.add_column("Rx (Mbps)", justify="right", style="green")

        for iface, data in stats.items():
            tx_mbps = self.calculate_speed(data["sent_bps"])
            rx_mbps = self.calculate_speed(data["recv_bps"])
            table.add_row(iface, str(tx_mbps), str(rx_mbps))
            
        return table

    def alert_threshold(self, max_mbps):
        stats = self.get_interface_stats()
        alerts = []
        for iface, data in stats.items():
            tx = self.calculate_speed(data["sent_bps"])
            rx = self.calculate_speed(data["recv_bps"])
            if tx > max_mbps or rx > max_mbps:
                alerts.append(f"ALERT: Interface {iface} exceeded {max_mbps} Mbps (Tx: {tx}, Rx: {rx})")
        return alerts

def live_monitor(interval=1):
    monitor = BandwidthMonitor()
    with Live(monitor.generate_report(), refresh_per_second=1) as live:
        while True:
            time.sleep(interval)
            live.update(monitor.generate_report())
