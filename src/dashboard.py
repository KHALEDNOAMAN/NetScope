from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio
import json

from .bandwidth_monitor import BandwidthMonitor
from .scanner import scan_network
from .topology import TopologyMapper

app = FastAPI(title="NetScope Dashboard")

monitor = BandwidthMonitor()

@app.get("/api/scan")
def api_scan(subnet: str = "192.168.1.0/24"):
    return scan_network(subnet)

@app.get("/api/topology")
def api_topology(subnet: str = "192.168.1.0/24"):
    mapper = TopologyMapper()
    mapper.discover_neighbors(subnet)
    return mapper.build_graph()

@app.websocket("/ws/bandwidth")
async def websocket_bandwidth(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            stats = monitor.get_interface_stats()
            formatted = {
                iface: {
                    "tx_mbps": monitor.calculate_speed(data["sent_bps"]),
                    "rx_mbps": monitor.calculate_speed(data["recv_bps"])
                } for iface, data in stats.items()
            }
            await websocket.send_json(formatted)
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket Error: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
