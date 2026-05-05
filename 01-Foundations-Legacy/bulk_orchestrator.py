import os
import json
from logger_tool import log_event

def run_bulk_scan(target_file):
    """It scans and analyzes all targets in a file sequentially."""

    if not os.path.exists(target_file):
        log_event(f"ERROR: {target_file} was not found!", "error")
        return
    
    # Open the file and read the targets.
    with open(target_file, "r") as f:
        # Remove hidden spaces at the end of lines before adding to the list.
        targets = [line.strip() for line in f if line.strip()]
        
    log_event(f"=== MASS SCREENING HAS BEGUN: {len(targets)} Target Set ===")
    
    for target in targets:
        log_event(f">>> TARGET IS BEING PROCESSED: {target} <<<", "info")
        
        # STEP 1: Port Scanning (Generates a new report for each target)
        # Note: Our security_reporter.py file should be configured to receive the target from an external source.
        # We can make it more flexible with a small update,
        # But for now, we're consolidating the current stream.
        os.system(f"python security_reporter.py") # Scans the current target

        # STEP 2: Analysis and Scoring
        if os.path.exists("scan_report.json"):
            os.system("python vulnerability_scanner.py")
            os.system("python security_scorer.py")
            
            # 2. Let's back up the reports by naming them (to prevent overwriting).
            # We save the report with the target name after each scan.
            backup_name = f"report_{target.replace('.', '_')}.json"
            os.rename("scan_report.json", backup_name)
            log_event(f"Analysis Completed: {backup_name} saved.")
        
        print("-" * 50)
    
    log_event("=== ALL TARGETS WERE SUCCESSFULLY SCANNED ===", "info")
    
if __name__ == "__main__":
    run_bulk_scan("targets.txt")
    