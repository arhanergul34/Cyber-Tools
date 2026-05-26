import scapy.all as scapy

class DnsTunnelingDetector:
    def __init__(self, pcap_file_path, length_threshold=30):
        self.pcap_file_path = pcap_file_path
        # Character length limit for a DNS query to be considered suspicious.
        self.length_threshold = length_threshold
        # How many unusual requests were sent to each domain? { "domain": request_count }
        self.dns_memory = {}
    
    def detect_tunneling(self):
        print(f"[*] Threat Hunting initiated for DNS Tunneling on: {self.pcap_file_path}")
        print(f"[*] Analyzing query string lengths (Threshold: >{self.length_threshold} characters)")
        print("=" * 75)
        
        try:
            packets = scapy.rdpcap(self.pcap_file_path)
            alerts_triggered = 0
            
            for index, packet in enumerate(packets):
                # If the packet contains a DNS layer and it is a Request packet
                if packet.haslayer(scapy.DNS) and packet[scapy.DNS].qr == 0:
                    # Get the queried website name and convert it to text.
                    query_name = packet[scapy.DNS].qname.decode(errors='ignore')
                    
                    # Cyber ​​Analysis: Does the length of the query cross our red line?
                    if len(query_name) > self.length_threshold:
                        alerts_triggered += 1
                        src_ip = packet[scapy.IP].src if packet.haslayer(scapy.IP) else "Unknown"
                        
                        print(f"\n[🚨 DNS EXFILTRATION ALERT #{alerts_triggered}]")
                        print(f"[-] Packet Number: #{index}")
                        print(f"[-] Source Client: {src_ip}")
                        print(f"[-] Suspicious Long Query ({len(query_name)} characters)")
                        print(f"    -> {query_name.strip()}")
                        print("-" *75)
            
            print(f"\n[+] Threat Hunt Complete. Total anomalous DNS activites logged: {alerts_triggered}")
        
        except FileNotFoundError:
            print(f"[-] Error: {self.pcap_file_path} not found.")

if __name__ == "__main__" :
    # We are subjecting our actual cyber analysis .pcap file to this test as well.
    detector = DnsTunnelingDetector(pcap_file_path="attack_traffic.pcap", length_threshold=25)
    detector.detect_tunneling()
    
               