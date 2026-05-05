class SecurityScanner:
    """
    Cybersecurity Scanner Class.
    This structure brings together the scanner's features (IP, Port) and
    capabilities (Scanning, Reporting) under a single umbrella.
    """
    
    def __init__(self, target_ip):
        # The 'initiator' method that runs when an object is created
        self.target_ip = target_ip
        self.open_ports = []
        print(f"Browser object created for [LOG] {self.target_ip}")
        
    def scan(self):
        # Scanning capability (Method)
        print(f"[*] {self.target_ip} scanning... Please Wait.")
        # Let's pretend we've found a few ports as a simulation.
        self.open_ports = [22, 80, 443]
        
    def report(self):
        # Reporting capability (Method)
        print(f"\n--- SECURITY REPORT: {self.target_ip} ---")
        if self.open_ports:
            print(f"[!] Open Ports Detected: {self.open_ports}")
        else:
            print("[✓] No Open Port Found.")
            
# --- RUNNING THE PROGRAM ---
if __name__ == "__main__":
    # 1. We create the object (We set up our machine)
    my_scanner = SecurityScanner("192.168.1.105")
    
    # 2. We are using their talents.
    my_scanner.scan()
    my_scanner.report()
    