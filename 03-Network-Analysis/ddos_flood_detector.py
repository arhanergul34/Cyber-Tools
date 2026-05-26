import scapy.all as scapy

class DdosFloodDetector:
    def __init__(self, pcap_file_path, flood_threshold=50):
        self.pcap_file_path = pcap_file_path
        # The minimum number of SYN packets an IP must send to be considered a DDoS attacker
        self.flood_threshold = flood_threshold
        # Memory Log: { "ip_address": syn_packet_count }
        self.flood_memory = {}
    
    def detect_ddos(self):
        print(f"[*] Threat Hunting initiated for DDoS/SYN Flood on: {self.pcap_file_path}")
        print(f"[*] Setting Flood Threshold: >{self.flood_threshold} SYN packets...")
        print("=" *75)
        
        try:
            packets = scapy.rdpcap(self.pcap_file_path)
            ddos_detected = False
            
            for index, packet in enumerate(packets):
                # If the packet contains IP and TCP layers
                if packet.haslayer(scapy.IP) and packet.haslayer(scapy.TCP):
                    src_ip = packet[scapy.IP].src
                    # Set the TCP flag (S stands for SYN packet)
                    tcp_flag = packet[scapy.TCP].flags
                
                if tcp_flag == "S":
                    # If this is the first time we've seen this IP address, start the counter with 0.
                    if src_ip not in self.flood_memory:
                        self.flood_memory[src_ip] = 0
                    
                    # Increment the counter by 1 for every captured SYN packet.
                    self.flood_memory[src_ip] += 1
            
            # Reporting and Cyber ​​Decision Step
            for ip, syn_count in self.flood_memory.items():
                if syn_count >= self.flood_threshold:
                    ddos_detected = True
                    print(f"\n[🚨 DDoS FLOOD ALARM] High Volume SYN Activity Detected!")
                    print(f"[-] Attacker IP: {ip}")
                    print(f"[-] Total SYN Packets Sent: {syn_count}")
                    print(f"[-] Security Note: Potential DoS/DDoS source exhausting system resources.")
                    print("-" *75)
            
            if not ddos_detected:
                print("[+] Analysis Complete. No malicious SYN flood fingerprints found.")
            
        except FileNotFoundError:
            print(f"[-] Error: The file '{self.pcap_file_path}' was not found.")
            
if __name__ == "__main__":
    # We're putting our network analysis file through this massive test as well!
    detector = DdosFloodDetector(pcap_file_path="attack_traffic.pcap", flood_threshold=30)
    detector.detect_ddos()            