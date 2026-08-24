import networkx as nx
from scapy.all import sr1, IP, ICMP
import json

class TopologyMapper:
    def __init__(self):
        self.graph = nx.Graph()

    def discover_neighbors(self, subnet):
        from .scanner import scan_network
        hosts = scan_network(subnet)
        
        # Assume current machine is node 0 (Gateway typically)
        gateway = self.detect_gateway()
        self.graph.add_node(gateway, type="gateway")
        
        for host in hosts:
            self.graph.add_node(host['ip'], mac=host['mac'], hostname=host['hostname'], type="host")
            self.graph.add_edge(gateway, host['ip'])
            
    def detect_gateway(self):
        # A simple ping to an external IP with TTL=1 can reveal the default gateway
        pkt = IP(dst="8.8.8.8", ttl=1)/ICMP()
        reply = sr1(pkt, timeout=2, verbose=False)
        if reply:
            return reply.src
        return "Unknown Gateway"

    def build_graph(self):
        return nx.node_link_data(self.graph)

    def export_json(self, filename="topology.json"):
        data = self.build_graph()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        return filename
