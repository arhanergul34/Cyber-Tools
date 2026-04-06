# We define the function (Packaging Stage)
def scan_port(ip_address, port):
    print(f"--- [SCANNING] Checking {ip_address} on Port: {port} ---")
    # Let's run a fake check here.
    if port == 80:
        return "OPEN (HTTP Service Found)"
    else:
        return "CLOSED"
    
# We use the function (Recall Stage)
target = "192.168.1.10"
test_port = 80

result = scan_port(target, test_port)

print(f"[!] Scan Result: Port {test_port} on {target} is {result}")
    

