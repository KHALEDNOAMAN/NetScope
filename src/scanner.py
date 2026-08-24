import socket
from scapy.all import ARP, Ether, srp, conf
from rich.table import Table
from rich.console import Console

console = Console()

class PortScanner:
    def __init__(self, target):
        self.target = target
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]

    def scan(self):
        open_ports = []
        for port in self.common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        return open_ports

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"

def scan_network(subnet):
    conf.verb = 0
    arp_request = ARP(pdst=subnet)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients = []
    for element in answered_list:
        ip = element[1].psrc
        mac = element[1].hwsrc
        hostname = get_hostname(ip)
        clients.append({"ip": ip, "mac": mac, "hostname": hostname})

    table = Table(title=f"Network Scan Results ({subnet})")
    table.add_column("IP Address", style="cyan")
    table.add_column("MAC Address", style="magenta")
    table.add_column("Hostname", style="green")

    for client in clients:
        table.add_row(client['ip'], client['mac'], client['hostname'])

    console.print(table)
    return clients

if __name__ == "__main__":
    scan_network("192.168.1.0/24")
