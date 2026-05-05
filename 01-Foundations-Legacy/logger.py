import datetime

# File writing function only for open ports.
def log_open_port(message):
    with open("scan_reports.txt", "a") as file:
        file.write(f"[{datetime.datetime.now()}] {message}\n")

def log_separator():
    with open("scan_reports.txt", "a") as file:
        file.write(f"\n--- Scanning start: {datetime.datetime.now()} ---\n")
         
           
        