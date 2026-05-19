import scapy.all as scapy

class ArpMitmDefender:
    def __init__(self, interface=None):
        self.interface = interface
        # We record the actual IP and MAC address mapping of the modem on the network here.
        # In a secure network, the modem's actual MAC address is static.
        self.real_gateway_ip = "192.168.0.1"
        self.real_gateway_mac = "aa:bb:cc:dd:ee:ff"  
        
    def process_arp_packet(self, packet):
       """A function that passes every incoming ARP packet through a cybersecurity filter."""
       # STEP 1: Does the packet contain an ARP layer?
       if packet.haslayer(scapy.ARP):
           # STEP 2: Is this packet a REPLY packet? (op=2)
           if packet[scapy.ARP].op == 2:
                # We extract the IP and MAC addresses of the packet sender.
                sender_ip = packet[scapy.ARP].psrc # Protocol Source (Sender IP)
                sender_mac = packet[scapy.ARP].hwsrc # Hardware Source (Sender MAC)
               
            # STEP 3: Attack Analysis (Critical Point)
            # If the incoming response claims, "I am 192.168.1.1," but the MAC address it provides
            # differs from the MAC address of the actual modem that we know...
                if sender_ip == self.real_gateway_ip and sender_mac != self.real_gateway_mac:
                    print(f"\n[!!!!] CRITICAL SECURITY ALERT: ARP SPOOFING DETECTED! [!!!!]")
                    print(f"[*] Fake Gateway MAC Address: {sender_mac}")
                    print(f"[*] Someone is trying to intercept your network traffic (MITM)!\n")
                else:
                    # If normal, harmless ARP traffic is flowing, silently tap the screen.
                    print(f"[*] Normal ARP Reply: {sender_ip} is at {sender_mac}")
                    
    def start_defense(self):
        """The trigger function that places the network card in listening mode.""" 
        print(f"\n[*] ARP MITM Defender active on interface: {self.interface}\n")
        print("[*] Monitoring ARP tables for poisonous updates...\n")
        
        # store=False: We do not store packets to avoid straining the computer's RAM.
        # prn: Our pipeline that shoots every captured ARP packet up to the inspection room above!
        scapy.sniff(iface=self.interface, filter="arp", store=False, prn=self.process_arp_packet)
        
if __name__ == "__main__":
    # Since we are using Windows, we set interface=None.
    defender = ArpMitmDefender(interface=None)
    defender.start_defense()
               
                
                