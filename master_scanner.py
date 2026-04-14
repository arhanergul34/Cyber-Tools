import socket

def full_port_scanner(ip, start_port, end_port):
    # We print to the terminal that an IP address has been scanned.
    print(f"\n[>>>] TARGET IDENTIFIED: {ip} scanning...")
    
    for port in range(start_port, end_port + 1):
        soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soket.settimeout(0.3) 
        
        result = soket.connect_ex((ip, port))
        
        if result == 0:
            print(f"[+] {ip} -> Port [port] OPEN")
       
         
        soket.close()

#Step 1: Safely read the target file.    
try:
    with open("target_list1.txt", "r") as file:
        targets = file.readlines()
        print(f"[!] A total of {len(targets)} targets have been loaded.")
        
        # Step 2: Run the scan for each target.
        for target in targets:
            ip = target.strip()
            if ip: 
                full_port_scanner(ip, 20, 80)
                
except FileNotFoundError:
    print("[-] ERROR: 'target_list.1.txt file not found!")
    
print("\n[!] All targets scanned. The operation was completed successfully")


        