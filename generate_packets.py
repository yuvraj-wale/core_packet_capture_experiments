from scapy.all import IP, UDP, send
import time

def generate_packets(src_ip, dst_ip, src_port, dst_port, packet_count, rate_mbps):
    packet = IP(src=src_ip, dst=dst_ip) / UDP(sport=src_port, dport=dst_port)
    interval = 1 / (rate_mbps * 1000 / 8 / len(packet))

    for _ in range(packet_count):
        send(packet, iface='lo', verbose=False)
        time.sleep(interval)

if __name__ == "__main__":
    src_ip = "127.0.0.1"
    dst_ip = "127.0.0.1"
    src_port = 12345
    dst_port = 12001
    packet_count = 1000
    rate_mbps = 1  # 1 Mbps

    generate_packets(src_ip, dst_ip, src_port, dst_port, packet_count, rate_mbps)
