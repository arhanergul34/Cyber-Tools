import scapy.all as scapy  # The main engine for packaging production.
import sys

class PacketWizard:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        
    def send_custom_ping(self):
        """
        Creates and sends a customized ICMP (Ping) packet.
        We can add a hidden message inside the packet data!
        """
        print(f"[*] Sending custom ICMP packet to {self.target_ip}")
        
        # IP Layer: The target is determined
        # ICMP Layer: The type (Echo Request) is determined
        # Raw Layer: We insert a hidden 'payload' (message) inside the packet
        packet = scapy.IP(dst=self.target_ip) / scapy.ICMP() / scapy.Raw(load="Just Security Test")
        
        # Send the packet and wait for the response
        response = scapy.sr1(packet, timeout=2, verbose=False)
        
        if response:
            print(f"[+] Response received from {response.src}")
            # Can we read the hidden message inside the response packet?
            if response.haslayer(scapy.Raw):
                print(f"[!] Data inside response: {response[scapy.Raw].load.decode()}")
        else:
            print("[-] No response. The target might be filtering ICMP")
    
    def send_xmas_scan_packet(self, port):
        """
        Sends an 'Xmas Tree' packet (FIN, PSH, and URG flags set).
        It's called Xmas because it lights up all the flags like a Christmas tree!
        Used to bypass some old firewall rules.
        """
        print(f"[*] Sending Xmas packet to port {port}...")
        xmas_packet = scapy.IP(dst=self.target_ip) / scapy.TCP(dport=port, flags="FPU")
        
        response = scapy.sr1(xmas_packet, timeout=2, verbose=False)
        
        if response is None:
            print(f"[+] Port {port} is likely Open|Filtered (No response to Xmas)") 
        elif response.haslayer(scapy.TCP):
            if response.getlayer(scapy.TCP).flags == 0x14: # RST-ACK
                print(f"[-] Port {port} is Closed (Received RST)")
                
if __name__ == "__main__":
    target = "192.168.1.1"
    wizard = PacketWizard(target)
    
    print("--- ICMP Manipulation ---")
    wizard.send_custom_ping()
    
    print("\n--- TCP Xmas Manipulation ---")
    wizard.send_xmas_scan_packet(80)
       