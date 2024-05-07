import asyncio
from scapy.all import AsyncSniffer, Ether, DHCP
from queue import Queue
from threading import Thread
from typing import Any, Dict

# Define the entrypoint function
async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    interface = args.get("interface", "eth0")
    filter_criteria = args.get("filter", "udp dst port 67")

    # Thread-safe queue for inter-thread communication
    packet_queue = Queue()

    # Define a function to process packets in the main thread
    async def process_packets():
        while True:
            # Get the packet from the queue
            packet = packet_queue.get()
            if packet is None:
                # If the packet is None, stop processing
                break
            
            # Process the packet (extracting src MAC address and DHCP options)
            if packet.haslayer(Ether):
                src_mac = packet[Ether].src
                vendor_ident = None
                if packet.haslayer(DHCP) and type(packet[DHCP].options[3][1]) != list:
                    vendor_ident = packet[DHCP].options[3][1].decode('utf-8')
                else:
                    vendor_ident = packet[DHCP].options[3][1]
                event = {
                    "src_mac": src_mac,
                    "vendor_class_identifier": vendor_ident
                }
                # Put the event in the queue
                await queue.put(event)

    # Define a function to listen for packets and put them in the queue
    def listen_for_packets():
        # Define a callback function
        def packet_callback(packet):
            # Put the packet in the queue
            packet_queue.put(packet)

        # Start an asynchronous sniffer
        sniffer = AsyncSniffer(
            iface=interface,
            filter=filter_criteria,
            prn=packet_callback,
            store=False
        )
        sniffer.start()

        # Keep the sniffer running indefinitely
        try:
            while True:
                pass
        except KeyboardInterrupt:
            # If interrupted, stop the sniffer
            sniffer.stop()

    # Create a thread to listen for packets
    listener_thread = Thread(target=listen_for_packets)
    listener_thread.start()

    # Run the packet processing loop
    await process_packets()

    # Signal the listener thread to stop by putting None in the packet queue
    packet_queue.put(None)
    listener_thread.join()

# Test the plugin outside of ansible-rulebook
if __name__ == "__main__":
    class MockQueue:
        async def put(self, event):
            print(event)
    
    mock_arguments = {
        "interface": "eth0",
        "filter": "udp dst port 67"
    }
    
    asyncio.run(main(MockQueue(), mock_arguments))
