import socket            # Basic library for network connections
import json              # To save data in professional JSON format
from datetime import datetime   # To record when the report was generated
from concurrent.futures import ThreadPoolExecutor   # To perform simultaneous (fast) scanning

# A global list: We will gather all the results we found here.
scan_results = []

def grab_info(ip, port):
    """This line knocks on the door of a single port and asks for an identification card (banner)."""
    result_entry = {"port": port, "status": "CLOSED", "banner": None} # Create a data template for each port

    try:
        # Creating a TCP socket (IPv4, STREAM/TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0) # Response waiting time: 2 seconds

        # Connection attempt (successful if it returns 0)
        conneciton_status = s.connect_ex((ip, port))
        
        if conneciton_status == 0:
            result_entry["status"] = "OPEN" # Update status to 'OPEN'
            s.send(b'HEAD / HTTP/1.1\r\n\r\n') # Send a standard HTTP request to initiate communication with the service.

            # Take the raw data and convert it to readable text (ignore errors)
            raw_banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            result_entry["banner"] = raw_banner if raw_banner else "No banner"
            
        s.close()    # Close the socket (ensure resource management)
    except Exception as e:
        result_entry["error"] = str(e) # Record if an unexpected error occurs

    scan_results.append(result_entry) # Add the obtained information to the main list
    print(f"[*] Port {port} analysis completed.")
    
def save_report(target):
    """Professionally writes the collected data into a JSON file."""
    report_data = {
        "target": target,
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # Add timestamp
        "findings": scan_results        # Add all port data found
    }
    
    # Write data to 'scan_report.json' file
    with open("scan_report.json", "w") as f:
        json.dump(report_data, f, indent=4)   # Save in indentation (readable format)

    print(f"\n[+] Report created successfully: scan_report.json")

if __name__ == "__main__":
    target_ip = "scanme.nmap.org"   # Our test target (Real server)
    ports_to_scan = [22, 80, 443]   # Critical ports to be analyzed

    print(f"--- Security analysis has started for {target_ip} ---")
    
    # We are speeding up by using thread pooling
    with ThreadPoolExecutor(max_workers=5) as executor:
        for p in ports_to_scan:
            executor.submit(grab_info, target_ip, p)
    
    save_report(target_ip)   # Save the report once the scan is complete
