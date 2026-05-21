import scapy.all as scapy
class PcapHackerDetector:
    def __init__(self, pcap_file_path):
        # We store the file path of the PCAP file to be analyzed in memory.
        self.pcap_file_path = pcap_file_path
        # A dictionary (Piggy Bank) to store the IP addresses on the network and the number of packets they have sent.
        self.ip_packet_counts = {}
        
    def analyze_traffic(self):
        """A function that parses a PCAP file line by line and calculates the packet counts."""
        print(f"[*] Reading and parsing PCAP file: {self.pcap_file_path}")
        try:
            # STEP 1: Load the file into memory
            packets = scapy.rdpcap(self.pcap_file_path)
            print(f"[+] Successfully loaded {len(packets)} packets. Analyzing...")
            # STEP 2: Examine the packets one by one using the loop.
            for packet in packets:
                # If the packet contains an IP layer
                if packet.haslayer(scapy.IP):
                    source_ip = packet[scapy.IP].src # The IP that sent the packet
                    
                    # We save this IP address in our piggy bank (dictionary)
                    # If the IP is in the list, increase its count by 1, otherwise start from 0 and add 1
                    if source_ip in self.ip_packet_counts:
                        self.ip_packet_counts[source_ip] += 1
                    else:
                        self.ip_packet_counts[source_ip] = 1
                        
                
            # STEP 3: Report the Results on the Screen
            self.report_suspects()
        
        except FileNotFoundError:
            print(f"[-] Error: The file {self.pcap_file_path} was not found!")
    
    def report_suspects(self):
        """A function that analyzes the data in the piggy bank and identifies the hacker."""
        print("\n=== TRAFFIC ANALYSIS REPORT ===")
        print(f"{'IP Address':<20} | {'Packet Count':<12}")
        print("-" * 35)
        
        # We are listing all IPs and packet counts currently in the piggy bank.
        for ip, count in self.ip_packet_counts.items():
            print(f"{ip:<20} | {count:<12}")
        
        # Cyber ​​Intelligence Step: Identifying the IP sending the most packets (Anomaly Detection)
        if self.ip_packet_counts:
            hacker_ip = max(self.ip_packet_counts, key=self.ip_packet_counts.get)
            max_packets = self.ip_packet_counts[hacker_ip]
            
            print("-" * 35)
            print(f"[!!!] Digital Forensics Alert [!!!!]")
            print(f"[*] Suspicious IP generating the highest traffic: {hacker_ip}")
            print(f"[*] Number of Packages Sent: {max_packets}")
            print("[*] This IP address may have performed a DoS attack or port scan on the network!")
            
if __name__ == "__main__":
    detector = PcapHackerDetector("attack_traffic.pcap")
    detector.analyze_traffic()
                    
            
            
        
        

            