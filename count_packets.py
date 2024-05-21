from scapy.all import rdpcap

def count_packets(filename):
    packets = rdpcap(filename)
    packet_count = len(packets)
    print(f"Total packets captured: {packet_count}")
    return packet_count

if __name__ == "__main__":
    pcap_file = 'captured_packets.pcap'  # Path to your pcap file
    count_packets(pcap_file)
