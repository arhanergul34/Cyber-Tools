import re

class RegexPiiDetector:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        # PII (Personal Data) Cyber-Profile Definitions
        self.pii_patterns = [
            ("CREDIT_CARD", r"\b\d{4}[-\s]?\d{4}[-\s]?d{4}[-\s]?\d{4}\b", "Unencrypted credit card number found in log!"),
            ("EMAIL_ADDRESS", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "An email address has made its way into the system records!"),
            ("TC_KIMLIK", r"\b[1-9]\d{10}\b", "A Turkish National ID number has been detected in the logs!"),
        ]
    
    def scan_log_file(self):
        print(f"[*] Data Leekage Prevention (DLP) Scan started on: {self.log_file_path}")
        print("[*] Monitoring logs for forbidden PII (Personally Identifiable Information)...")
        print("=" * 75)
        
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as file:
                leak_count = 0
                
                # Read the file line by line, stripping away whitespace (Cyber ​​Hygiene!)
                for line_number, current_line in enumerate(file, 1):
                    current_line = current_line.strip()
                    
                    # Test each personal data pattern on the row.
                    for pii_type, pattern, description in self.pii_patterns:
                        
                        if re.search(pattern, current_line):
                            leak_count += 1 
                            print(f"\n[🚨 PII LEAK ALERT #{leak_count}] Type: {pii_type}")
                            print(f"[-] Location: Line {line_number}")
                            print(f"[-] Leaked Log: {current_line}")
                            print(f"[-] Risk Note: {description}")
                            print("=", 75)
            
            # Final Report (Completely outside the loop!)
            if leak_count == 0:
                print("\n[+] DLP Scan Finished. No sensitive PII leaks found in log files.")
            else:
                print(f"\n[+] DLP Scan finished. Total sensitive data leaks intercepted: {leak_count}")   
        
        except FileNotFoundError:
            print(f"[-] Error: Log file '{self.log_file_path}' could not be found.")
            
if __name__ == "__main__":
    # To test it, we first start the vehicle itself.
    detector = RegexPiiDetector(log_file_path="server_logs.txt")
    detector.scan_log_file()
                           