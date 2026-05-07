from scapy.all import IP, ICMP, Raw, send # Added the Raw library

class NetworkCrafter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.packet = None
        
    def create_ping_packet(self):
        # The data we will hide inside the packet (Payload)
        secret_message = "BERLIN-INTERN-2026-READY"
        
        # Stacking the layers: IP / ICMP / RAW DATA
        self.packet = IP(dst=self.target_ip) / ICMP() / Raw(load=secret_message)
        
        print(f"[+] The package has been prepared. Message: {secret_message}")
        
    def send_packet(self):
        if self.packet:
            send(self.packet)
            print(f"[✓] Message packet launched to {self.target_ip}")
            
if __name__ == "__main__":
    crafter = NetworkCrafter("8.8.8.8")
    crafter.create_ping_packet()
    crafter.send_packet()
    
    