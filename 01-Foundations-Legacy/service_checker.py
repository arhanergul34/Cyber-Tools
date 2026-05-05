import socket
from concurrent.futures import ThreadPoolExecutor

# STEP 1: Job Description (Request ID Card)
def grab_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3.0) # We are giving you a little more time for banner responses.
        s.connect((ip, port))
        # Some services send a banner as soon as a connection is established. 
        # Others require you to say "Hello" (e.g., \r\n).
        s.send(b'Hello\r\n')

        # We are receiving the first 1024 bytes of response.
        raw_data = s.recv(1024)
        
        # CRITICAL POINT: Even if the incoming data is not text, do not give an error; try to decode it.
        # If you cannot decode it (errors='ignore'), only show the readable parts.
        banner = raw_data.decode('utf-8', errors='ignore').strip()
        
        if banner:
            print(f"[+] PORT {port} ID: {banner}")
        else:
            print(f"[!] PORT {port}: Connection established, but no banner received.")
    
        s.close()
        
    except socket.timeout:
        print(f"[-] PORT {port}: Timeout (No response)")    
    except Exception as e:
        print(f"[!] PORT {port} Error: {e}")
         
        
    
# STEP 2: Operations Center
def identify_services(target_ip, target_ports):
    print(f"--- Service analysis has started on {target_ip} ---")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        for port in target_ports:
            executor.submit(grab_banner, target_ip, port)
            
# STEP 3: Main Run
if __name__ == "__main__":
    target = "scanme.nmap.org"
    test_ports = [22, 80]
    identify_services(target, test_ports)
          
