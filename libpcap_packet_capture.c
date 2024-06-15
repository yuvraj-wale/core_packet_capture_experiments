#include <pcap.h>
#include <stdio.h>
#include <signal.h>
#include <sys/types.h>

volatile int packet_count = 0;  
pcap_t *handle;              

void packet_handler(u_char *user_data, const struct pcap_pkthdr *pkthdr, const u_char *packet) {
    packet_count++;
}

void signal_handler(int signum) {
    printf("Captured %d packets\n", packet_count);
    pcap_breakloop(handle); 
}

int main() {
    char *dev = "lo";
    char errbuf[PCAP_ERRBUF_SIZE];
    
    // Open device for capturing
    handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
    if (handle == NULL) {
        fprintf(stderr, "Couldn't open device %s: %s\n", dev, errbuf);
        return 2;
    }
    
    // Set signal handler
    signal(SIGINT, signal_handler);
    
    // Capture packets
    pcap_loop(handle, 0, packet_handler, NULL);
    
    // Close handle
    pcap_close(handle);
    
    return 0;
}
