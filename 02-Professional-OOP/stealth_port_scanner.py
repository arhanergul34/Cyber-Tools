import scapy.all as scapy

class StealthPortScanner:
    def __init__(self, target_ip):
        # We are storing the target computer's IP address in our persistent memory.
        self.target_ip = target_ip
        # List of critical ports we want to scan
        self.ports_to_scan = [21, 22, 23, 25, 80, 443, 8080]
    
    def scan_port(self, port):
        """
        A function that stealthily (SYN) scans a single port.
        """
        # STEP 1: We construct the spoofed SYN packet
        # We specify the target at the IP layer, the port at the TCP layer, and the spoofed "S" (SYN) flag.
        syn_packet = scapy.IP(dst=self.target_ip) / scapy.TCP(dport=port, flags="S")
        
        # STEP 2: Send the packet and wait for the response (sr1: send and receive 1 packet)
        # timeout=1: If no response is received within 1 second, assume the host is down
        # verbose=False: Prevent Scapy from printing verbose output to the screen
        response = scapy.sr1(syn_packet, timeout=1, verbose=False)
        
        # STEP 3: Analyze the response received
        if response is not None:
            # If the incoming packet contains a TCP layer
            if response.haslyer(scapy.TCP):
                # We check the flags of the incoming packet.
                # If the other party has responded with "SA" (SYN-ACK): they are essentially saying, "The door is open; come on in!"
                if response[scapy.TCP].flags == "RA":
                    # Since the port is closed, we are not printing any text to the screen to avoid clutter.
                    pass
                
    def start_scan(self):
        """The trigger function that initiates the scan."""
        print(f"\n[*] Stealth Port Scan started for target: {self.target_ip}")
        print("[*] Scanning critical ports without leaving traces...\n")
        
        # Using a loop, we send each port in the list, one by one, to the inspection room above.
        for port in self.ports_to_scan:
            self.scan_port(port)
            
        print("\n[+] Scan Completed Successfully.")

if __name__ == "__main__":
    scanner = StealthPortScanner(target_ip="192.168.1.1")
    scanner.start_scan()