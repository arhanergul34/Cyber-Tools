import re

class StaticCodeAnalyzer:
    def __init__(self, target_file_path):
        self.target_file_path = target_file_path
        # Cyber ​​Risk Signatures: (Error Type, Regex Pattern to Search, Security Note)
        self.vulnerability_signatures = [
            ("HARDCODED_SECRET", r"(password|passwd|secret|api_key)\s*=\s*['\"]", "A hidden password or API key may be embedded in the code!"),
            ("DANGEROUS_FUNCTION", r"\beval\(|\bexec\(", "Usage of the eval() or exec() function detected! Command Injection risk present."),
            ("INSECURE_MODULE", r"import\s+(md5|telnetlib|crypt)", "An outdated or insecure cyber library has been included in the project!")
        ]
    
    def analyze_file(self):
        print(f"[*] Initiating Static Code Analysis on: {self.target_file_path}")
        print("[*] Scanning for potential software vulnerabilities...")
        print("=" * 50)
        
        try:
            with open(self.target_file_path, 'r', encoding='utf-8') as file:
                findings_count = 0
                
                # Read each line in the file, along with its sequence number (Manager-Worker Logic)
                for line_number, current_line in enumerate(file, 1):
                    current_line = current_line.strip()
                    
                    # Test each cyber risk on this single line.
                    for vuln_type, pattern, description in self.vulnerability_signatures:
                        # The Regex engine searches the line for a dangerous pattern.
                        if re.search(pattern, current_line, re.IGNORECASE):
                            findings_count += 1
                            print(f"\n[🚨 VULNERABILITY ALERT #{findings_count}] Type: {vuln_type}")
                            print(f"[-] Location: Line {line_number}")
                            print(f"[-] Content: {current_line}")
                            print(f"[-] Security Note: {description}")
                            print("-" * 75)
            
            # Final Decision Step (Outside the Loop!)
            if findings_count == 0:
                print("\n[+] Analysis finished. No software vulnerability signatures detected. Code is secure!")
            else:
                print(f"\n[+] Analysis finished. Total security findings: {findings_count}")
        
        except FileNotFoundError:
            print(f"[-] Error: Target file '{self.target_file_path}' could not be found.")
            
if __name__ == "__main__":
    # To Test: We are scanning the code file we wrote ourselves with our own robot!
    analyzer = StaticCodeAnalyzer(target_file_path="static_code_analyzer.py")
    analyzer.analyze_file()
    