from scapy.all import IP, ICMP, send

class NetworkCrafter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.packet = None
        
    def create_ping_packet(self):
        # We stack the layers on top of each other (Just like in Wireshark!)
        # IP layer (Layer 3) + ICMP layer (Ping message)
        self.packet = IP(dst=self.target_ip) / ICMP()
        print(f"[+] Ping packet prepared for {self.target_ip}")
        
    def send_packet(self):
        if self.packet:
            print(f"[*] The package is on its way...")
            send(self.packet)
            print("[✓] The package was successfully sent.")

if __name__ ==  "__main__":
    # You can choose your own modem or Google (8.8.8.8) as the target.
    crafter = NetworkCrafter("8.8.8.8")
    crafter.create_ping_packet()
    crafter.send_packet()
          