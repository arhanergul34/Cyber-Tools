import scapy.all as scapy

class DnsAnalyser:
    def __init__(self, interface=None):
       # None for Windows, "eth0" for Linux.
       self.interface = interface 
       # Suspicious sites on the network that we have blacklisted and wish to monitor
       self.blacklist = ["malware.com", "bet-site.com", "phishing-bank.com"]
       
    def process_dns_packet(self, packet):
        """
        A function that analyzes each packet captured from the air.
        """
        # STEP 1: Check if the packet contains a DNS layer.
        if packet.haslyaer(scapy.DNS):
            # packet[scapy.DNS].qd: Is there a DNS Query?
            if packet [scapy.DNS].qd:
                # We retrieve the name of the website the victim wants to visit and sanitize it.
                requested_site = packet[scapy.DNSQR].qname.decode("utf-8").strip(".")
                
                print(f"[*] DNS Query Detected: The device is searching for this -> {requested_site}")
                
                # STEP 2: Blacklist Check
                for suspect in self.blacklist:
                    if suspect in requested_site:
                        print(f"\n[!] ALERT: The device is attempting to access a blacklisted site: {requested_site}!\n")
             
            # STEP 3: Capturing the Reply from the DNS Server
            # an: Is there an Answer layer? 
            if packet[scapy.DNS].an:
                # Read the real or fake target IP address contained within the response received from the DNS server.
                resolved_ip = packet[scapy.DNSRR].rdata
                print(f"[+] DNS Reply Detected: The site has been redirected to this IP -> {resolved_ip}") 
                
    def start_analysis(self):
        """The trigger function that starts sniffing the network."""
        print(f"[*] DNS Analyser started on interface: {self.interface}")
        print("[*] Monitoring DNS traffic for anomalies...")
        
        # We filter for UDP port 53 to capture only DNS packets.
        # prn: Specifies which function to pass each captured packet to (The pipeline!)
        scapy.sniff(iface=self.interface, filter="udp port 53", store=False, prn=self.process_dns_packet)
        
if __name__ == "__main__":
    # Since we are using Windows, we are passing None to the persistent memory slot.
    analyser = DnsAnalyser(interface=None)
    analyser.start_analysis()
            