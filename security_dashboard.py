import json
import os
from logger_tool import log_event

def load_report(file_name):
    """Uploads report files securely."""
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return None

def show_dashboard():
    print("\n" + "="*50)
    print("      🛡️ CYBER SECURITY COMMAND CENTER 🛡️")
    print("="*50)
    
    # 1. Check the Scanning Reports
    reports = [f for f in os.listdir() if f.startswith("report_") and f.endswith(".json")]
    print(f"\n[+] Total Number of Targets Analyzed: {len(reports)}")
    
    for r in reports:
        data = load_report(r)
        if data:
            target = data.get("target", "Unknown")
            
            # --- CRITICAL CORRECTION AREA (Type Casting) ---
            # We convert the data from the JSON to a number; if there is an error, we accept 0.
            try:
                score = int(data.get("security_score", 0))
            except (ValueError, TypeError):
                score = 0 
                
            level = data.get("risk_level", "LOW")
            
            # Set status icon
            status_icon = "🔴" if score < 50 else "🟡" if score < 80 else "🟢"
            print(f"{status_icon} Target: {target.ljust(20)} | Score: {score}/100 | Risk: {level}")
            
    # 2. System Log Summary
    print("\n" + "-"*50)
    print("📝 LATEST SYSTEM ACTIVITIES (Log Summary)")
    if os.path.exists("cyber_tool.log"):
        with open("cyber_tool.log", "r") as f:
            lines = f.readlines()
            # Show the last 5 activities
            for line in lines [-5:]:
                print(f" > {line.strip()}")
            
    print("\n" + "="*50)
    print("Operation Status: ON HOLD...")

if __name__ == "__main__":
    show_dashboard()    