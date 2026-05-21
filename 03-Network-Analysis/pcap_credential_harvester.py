import scapy.all as scapy

class PcapCredentialHarvester:
    def __init__(self, pcap_file_path):
        # Path to the target PCAP file to be analyzed
        self.pcap_file_path = pcap_file_path
        # A list of critical cyber keywords that hackers might search for or attempt to infiltrate.
        self.critical_keywords = ["user", "password", "pass", "login", "admin", "secret", "token"]
    
    def harvest_credentials(self):
        print(f"[*] Starting Credential Harvesting on: {self.pcap_file_path}")
        print(f"[*] Searching for unencrypted sensitive data...")
        print("=" *60)
        
        try:
            # Loading the PCAP file into memory
            packets = scapy.rdpcap(self.pcap_file_path)
            trigger_count = 0
            
            # Loop to examine each package individually
            for index, packet in enumerate(packets):
                # If the packet contains a raw data (message) layer
                if packet.haslayer(scapy.Raw):
                    # Load the raw data and convert it into readable text.
                    payload = packet[scapy.Raw].load.decode(errors='ignore')
                    
                    # Cyber ​​Intelligence Check: Do our "insidious words" appear within the text?
                    for keyword in self.critical_keywords:
                        if keyword in payload.lower():
                            trigger_count += 1
                            print(f"\n[ALERT #{trigger_count}] Sensitive Data Detected in Packet #{index}!")
                            
                            # If the packet has an IP layer, also add the sender and recipient to the report.
                            if packet.haslayer(scapy.IP):
                                print(f"[-] Source IP: {packet[scapy.IP].src} -> Destination IP: {packet[scapy.IP].dst}")
                            
                            print(f"[-] Triggered Keyword: '{keyword}'")
                            print(f"[-] Extracted Payload Data:\n{payload.strip()}")
                            print("-" *60)
                            break  # If there are multiple words in the same package, exit the loop to avoid cluttering the screen.
            
            print(f"\n[+] Analysis Completed. Total alerts raised: {trigger_count}") 
        
        except FileNotFoundError:
            print(f"[-] Error: {self.pcap_file_path} not found.")
            
if __name__ == "__main__":
    # We are also feeding the actual attack file we just used as bait here.
    harvester = PcapCredentialHarvester(pcap_file_path="attack_traffic.pcap")
    harvester.harvest_credentials()                                   