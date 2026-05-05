import socket

def full_port_scanner(ip, start_port, end_port):
    print(f"[...] {ip} scanning addresses...")
    
    # Loop: Scan through each number from the starting port to the ending port.
    for port in range(start_port, end_port + 1):
        soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soket.settimeout(0.5) # We shortened the time to increase scanning speed.
        
        result = soket.connect_ex((ip, port))
        
        if result == 0:
            print(f"[+] Port {port} OPEN")
        else:
            print(f"[!] Port {port} checked (CLOSED)")
            
        soket.close()
        
# Scan ports 20 through 80.
full_port_scanner("127.0.0.1", 20, 80)

