# STEP 1: Function that Stores the Data (Memory Unit)
def log_save(message):
    """
    This function receives the message and appends it as a new line to the end of the file.
    """
    with open("scan_reports.txt", "a", encoding="utf-8") as file:
         file.write(message + "\n")
         
# STEP 2: Targets (Data Set)
targets = ["192.168.1.1", "192.168.1.5", "10.0.0.15", "172.16.0.20"]
    
## STEP 3: Process Cycle (Automation)
print("---[SYSTEM] Logging process started... ---")

for ip in targets:
    # We are preparing our messeage
    log_msg = f"[INFO] Scanning target: {ip} - Status: COMPLETED"
    
    # We are printing to the screen (Live viewing)
    print(log_msg)
    
    # We also save it to a file by calling our function (Permanent save).
    log_save(log_msg)
    
    
    
print("--- [SYSTEM] All scans logged successfully. ---")
