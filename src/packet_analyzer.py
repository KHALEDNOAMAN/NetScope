from scapy.all import sniff, wrpcap, TCP, UDP, ICMP, IP, DNS
from collections import Counter
import time

class PacketAnalyzer:
    def __init__(self):
        self.packets = []
        self.protocols = Counter()
        self.top_talkers_src = Counter()
        self.top_talkers_dst = Counter()
        self.syn_count = Counter()

    def process_packet(self, packet):
        self.packets.append(packet)
        if IP in packet:
            self.top_talkers_src[packet[IP].src] += 1
            self.top_talkers_dst[packet[IP].dst] += 1
            
            if TCP in packet:
                self.protocols['TCP'] += 1
                if packet[TCP].flags == 'S':
                    self.syn_count[packet[IP].src] += 1
            elif UDP in packet:
                self.protocols['UDP'] += 1
                if DNS in packet:
                    self.protocols['DNS'] += 1
            elif ICMP in packet:
                self.protocols['ICMP'] += 1

    def capture_packets(self, interface, count=100, filter=""):
        sniff(iface=interface, prn=self.process_packet, count=count, filter=filter, store=False)

    def analyze_protocols(self):
        return dict(self.protocols)

    def get_top_talkers(self):
        return {
            "source": self.top_talkers_src.most_common(5),
            "destination": self.top_talkers_dst.most_common(5)
        }

    def detect_anomalies(self):
        anomalies = []
        for ip, count in self.syn_count.items():
            if count > 50:  # Arbitrary threshold for SYN flood/scan
                anomalies.append(f"Potential SYN flood/scan from {ip} ({count} SYN packets)")
        return anomalies

    def export_pcap(self, filename):
        if self.packets:
            wrpcap(filename, self.packets)
            return True
        return False
