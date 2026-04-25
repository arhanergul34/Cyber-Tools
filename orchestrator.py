import os # 1. It allows us to communicate with the computer using the command line.
import json # 2. It allows us to review report files.
from logger_tool import log_event # 3. We're bringing our logging skills from yesterday here.

def run_cyber_orchestra():
    """It is the main function that manages all cybersecurity tools in sequence."""

    # INTRODUCTION: Operation log is being kept.
    log_event("--- CYBER SECURİTY OPERATİON HAS BEGUN ---", "info")
    
    # STEP 1: DATA COLLECTION (Port Scanning)
    # This line will write 'python security_reporter.py' to the terminal instead of you.
    log_event("STEP 1: Port scanning and data collection are in progress...")
    os.system("python security_reporter.py")
    
    # STEP 2: DATA ANALYSIS (Vulnerability Detection) 
    # Architectural Control: Has the report file been generated?
    if os.path.exists("scan_report.json"):
        log_event("STEP 2: Scanning report found. Proceeding with vulnerability analysis...")
        os.system("python vulnerability_scanner.py")
    else:
        # If the first step fails, it stops the operation.
        log_event("ERROR: Report file not found! Operation stopped.", "error")
        return
    
    # STEP 3: EVALUATION (Safety Score)
    log_event("STEP 3: The analysis results are scored and the risk level is determined...")
    os.system("python security_scorer.py")
    
    # CLOSING: Final Log
    log_event("--- THE OPERATION WAS SUCCESSFULLY COMPLETED ---", "info")
    
if __name__ == "__main__":
    run_cyber_orchestra()
    

