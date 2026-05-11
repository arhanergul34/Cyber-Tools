from scapy.all import sniff, IP

class NetworkSniffer:
    def __init__(self):
        print("[*] Listener starting... Waiting for packets.")
        
    def packet_callback(self, packet):
        # Every captured packet falls into this function
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            print(f"[+] Packet Captured: {src_ip} -> {dst_ip}")
            
    def start_sniffing(self):
        # Listen until you catch 10 packages
        sniff(prn=self.packet_callback, count=10)
        
if __name__ == "__main__":
    my_sniffer = NetworkSniffer()
    my_sniffer.start_sniffing()
    
    