import socket

def port_scanner(ip, port):
    # SOCK_STREAM indicates that we are using the TCP protocol (Trusted connection)
    soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connection timeout (wait 1 second, close if no response)
    soket.settimeout(1)
    
    
    # Try to connect
    result = soket.connect_ex((ip, port))
    
    if result == 0:
        print(f"[+] Port {port} OPEN")
    else: 
        print(f"[-] Port {port} CLOSED")
        
    soket.close()
    
port_scanner("127.0.0.1", 80)
