import scapy.all as scapy

class ArpSpoofDetector:
    def __init__(self, pcap_file_path):
        self.pcap_file_path = pcap_file_path
        # Memory Notebook: { "ip_address": "actual_mac_address" }
        self.arp_mac_table = {}
    
    def detect_spoofing(self):
        print(f"[*] Threat Hunting initiated for ARP Spoofing (MITM) on: {self.pcap_file_path}")
        print("[*] Verifying IP-to-MAC address bindings for anomalies...")
        print("=" *75)
        
        try:
            packets = scapy.rdpcap(self.pcap_file_path)
            spoof_detected = False
            
            for index, packet in enumerate(packets):
                # If the packet contains an ARP layer and it is a Reply packet
                if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2: 
                    # Let's extract the IP and physical MAC addresses from the packet.
                    src_ip = packet[scapy.ARP].psrc
                    src_mac = packet[scapy.ARP].hwsrc
                    
                    # If we are seeing this IP in our logbook for the first time, let's record it.
                    if src_ip not in self.arp_mac_table:
                        self.arp_mac_table[src_ip] = src_mac
                        
                    # IF THIS IP HAS BEEN RECORDED PREVIOUSLY AND THE CURRENT MAC ADDRESS IS DIFFERENT!
                    elif self.arp_mac_table[src_ip] != src_mac:
                        spoof_detected = True
                        print(f"\n[🚨 MITM ARP SPOOF ALARM]")
                        print(f"[-] Packet Number: #{index}")
                        print(f"[-] Spoofed Target IP: {src_ip}")
                        print(f"[-] Legitimate MAC (Original): {self.arp_mac_table[src_ip]}")
                        print(f"[-] Fake/Attacker MAC (New):    {src_mac}")
                        print(f"[-] Security Note: Someone is trying to hijack network traffic via ARP Poisoning!")
                        print("-" *75)
                
            if not spoof_detected:
                    print("[+] Analysis complete. No ARP spoofing or MITM signatures detected.")
            
        except FileNotFoundError:
            print(f"[-] Error: {self.pcap_file_path} not found.")

if __name__ == "__main__":
    # We are putting that renowned cyber traffic from our arsenal through this test as well.
    detector = ArpSpoofDetector(pcap_file_path="attack_traffic.pcap")
    detector.detect_spoofing()

                            