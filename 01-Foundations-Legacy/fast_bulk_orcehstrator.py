import os
import threading  # 1. A library that allows us to do multiple tasks simultaneously.
from logger_tool import log_event

def process_target(target):
    """The function of a worker working alone for each objective."""
    log_event(f"[*] Worker Started: {target} scanning...")
    
    # 2. Run existing scan commands
    os.system(f"python security_reporter.py")
    
    # Back up the report immediately (Because other workers will be writing their own reports!)
    backup_name = f"fast_report_{target.replace('.', '_')}.json"
    if os.path.exists("scan_report.json"):
        os.rename("scan_report.json", backup_name)
        log_event(f"[✓] {target} completed and saved as {backup_name}")
        
def run_threaded_scan(target_file):
    if not os.path.exists(target_file):
        return
    
    with open(target_file, "r") as f:
        targets = [line.strip() for line in f if line.strip()]
        
    log_event(f"=== RAPID SCANNING HAS STARTED ({len(targets)} Target)")
    
    threads = []  # 3. A list to track workers
    
    for target in targets:
        # We create a new worker (thread) for each target.
        # The first 'target' in the target=target part is the name the function expects.
        t = threading.Thread(target=process_target, args=(target,))
        threads.append(t)
        t.start() # 4. Send the worker to work! (Moves on to the next one without delay)
        
    # 5. Wait for all workers to finish their work.
    for t in threads:
        t.join()
        
    log_event("=== ALL RAPID SCANS HAVE BEEN COMPLETED ===")

if __name__ == "__main__":
    run_threaded_scan("targets.txt")    



