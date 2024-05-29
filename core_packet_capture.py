from scapy.all import sniff

def packet_handler(packet):
    global packet_count
    packet_count += 1

def main():
    global packet_count
    packet_count = 0
    interface = 'lo'

    print(f"Starting packet capture on interface {interface}...")

    sniff(iface=interface, prn=packet_handler, store=False, count=0)

    print(f"Packet capture complete. {packet_count} packets captured.")

if __name__ == "__main__":
    main()
