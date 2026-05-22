import scapy.all as scapy

class PortScannerDetector:
    def __init__(self, pcap_file_path, port_threshold=10):
        self.pcap_file_path = pcap_file_path
        # The minimum number of distinct ports an IP address must target to be classified as an attacker (Threshold Value)
        self.port_threshold= port_threshold
        # Memory Room
        self.scanner_memory = {}
        
    def detect_scanners(self):
        print(f"[*] Analyzing {self.pcap_file_path} for Port Scanning activity...")
        print(f"[*] Detection Threshold: {self.port_threshold} distinct ports.")
        print("=" *65)
        
        try:
            packets = scapy.rdpcap(self.pcap_file_path)
            
            for packet in packets:
                # If the packet contains both IP and TCP layers
                if packet.haslayer(scapy.IP) and packet.haslayer(scapy.TCP):
                    src_ip = packet[scapy.IP].src
                    dst_port = packet[scapy.TCP].dport
                    
                    # We can exempt ourselves (the gateway/modem) from the scan list.
                    if src_ip == "192.168.1.254":
                        continue
                    
                    # If we are seeing this IP for the first time, let's make room for it in the piggy bank.
                    if src_ip not in self.scanner_memory:
                        self.scanner_memory[src_ip] = set()
                       
                    # Add the target port hit by the IP to the set (Does not add the same port again)
                    self.scanner_memory[src_ip].add(dst_port)
            
            # Cyber ​​Intelligence and Reporting Step
            scan_detected = False
            for ip, probed_ports in self.scanner_memory.items():
                distinct_port_count = len(probed_ports)
                
                # If the number of probed ports exceeds our defined threshold value
                if distinct_port_count >= self.port_threshold:
                    scan_detected = True
                    print(f"\n[RECON ALARM] Potential Port Scanner Detected !")
                    print(f"[-] Attacker IP: {ip}")
                    print(f"[-] Scanned Port Count: {distinct_port_count} distinct ports")
                    # Let's print the first 10 ports it probed, in order, to the screen.
                    sorted_ports = sorted(list(probed_ports))
                    print(f"[-] Target Ports (Sample): {sorted_ports[:10]}")
                    print("-"*65)

            if not scan_detected:
                print("[+] Analysis Completed. No port scanning signatures detected.")
        
        except FileNotFoundError:
            print("[-] Error: {self.pcap_file_path} not found.")
            
if __name__ == "__main__":
    # We are re-injecting the pre-generated attack traffic from our folder.
    detector = PortScannerDetector(pcap_file_path="attack_traffic.pcap", port_threshold=5)
    detector.detect_scanners()
    