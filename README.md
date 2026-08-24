# NetScope

Network Monitoring & Packet Analysis tool.

## Overview
NetScope is a comprehensive network monitoring and packet analysis tool designed for real-time traffic inspection, bandwidth monitoring, and network topology discovery.

## Features
- Real-time packet capture and analysis
- Bandwidth monitoring and alerting
- Network scanning and topology discovery
- Web dashboard and CLI interface

## Architecture
```
[CLI/Web] -> [Dashboard API] -> [Core Engine: Scanner/Analyzer/Monitor] -> [Network Interfaces]
```

## Tech Stack
- Python 3.11
- Scapy (Packet analysis)
- FastAPI (Web dashboard)
- psutil (System metrics)
- Rich & Click (CLI)

## Screenshots
```text
+-------------------------------------------------+
| NetScope CLI Dashboard                          |
|-------------------------------------------------|
| Bandwidth: 15.2 Mbps [||||||||||      ]         |
| Active Hosts: 24                                |
| Anomalies: 0                                    |
+-------------------------------------------------+
```

## Installation
```bash
git clone https://github.com/KHALEDNOAMAN/NetScope.git
cd NetScope
pip install -r requirements.txt
python setup.py install
```

## Usage
CLI:
```bash
netscope scan 192.168.1.0/24
netscope monitor --interface eth0
```

## How It Works
NetScope utilizes Scapy for raw socket packet capture and psutil for cross-platform interface statistics. The FastAPI backend serves real-time data via WebSockets to the frontend.

## Roadmap
- [ ] Add BPF filter support for packet capture
- [ ] Implement ML-based anomaly detection
- [ ] Enhance web dashboard with D3.js topology maps

## License
MIT License
