from scapy.all import sniff, wrpcap

def packet_handler(packet):
    packets.append(packet)

def main():
    global packets
    packets = []
    interface = 'lo'  # Loopback interface
    port_filter = 'port 12001'  # Capture packets on port 12001

    print(f"Starting packet capture on interface {interface} with filter '{port_filter}'...")

    # Capture packets on the 'lo' interface
    sniff(iface=interface, prn=packet_handler, store=True, count=0, filter=port_filter)

    # Dump all captured packets to a pcap file
    wrpcap('captured_packets.pcap', packets)

    print("Packet capture complete. Data saved to captured_packets.pcap")

if __name__ == "__main__":
    main()
