import socket
from concurrent.futures import ThreadPoolExecutor
import time

# STEP 1: Task Definition (Check a single port)
def scan_port(ip, port):
    try:
        # Socket creation (IPv4, TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0) # Bekleme süresi (Hız için kısa tuttuk)
        
        # Connection attempt (port is open if it returns 0)
        result = s.connect_ex((ip, port)) 
        
        if result == 0:
            print(f"[+] PORT FOUND: {ip} -> {port} OPEN")    
        else:
            print(f"[-] {port} CLOSED") 
               
            s.close()
    except Exception:
        pass ## Silently ignore errors (Prevent network noise)

# STEP 2: Operations Center
def run_fast_scan(target_ip, port_range):
    print(f"---Quick scan initiated for {target_ip} ---")
    start_time = time.time()
    
    # ARCHITECTURE HERE: Check 20 ports simultaneously!
    with ThreadPoolExecutor(max_workers=20) as executor:
        for port in port_range:
            executor.submit(scan_port, target_ip, port)
            
    end_time = time.time()
    print(f"\n[!] The scan was completed in {end_time - start_time:.2f} seconds.")
    
# STEP 3: Main Run
if __name__ == "__main__":
    target = "127.0.0.1"
    ports = [135, 139, 445, 80, 443, 3306, 3389]    
    
    run_fast_scan(target, ports)