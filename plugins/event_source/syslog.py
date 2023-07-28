import asyncio
import socketserver
from typing import Any, Dict

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.request[0])

async def run_udp_server(queue: asyncio.Queue, args: Dict[str, Any]):
    host = args.get("host", "0.0.0.0")
    port = args.get("port", 514)

    with socketserver.UDPServer((host, port), MyUDPHandler) as server:
        await queue.put(self.request[0])

if __name__ == "__main__":
    class MockQueue:
        async def put(self, event):
            print(event)

    mock_arguments = {"host": "0.0.0.0", "port": 514, "delay": 1}
    asyncio.run(run_udp_server(MockQueue(), mock_arguments))
