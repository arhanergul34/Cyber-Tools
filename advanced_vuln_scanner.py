import json
import re

# STEP 1: Vulnerability Database (We made it a bit smarter)
# Here we keep the versions as keys.
VULN_CATALOG = {
    "2.4.7": "CRITICAL: Apache Heartbleed Vulnerability!",
    "1.1.1": "HIGH: SSL Certificate Validation Issue.",
    "8.2": "MEDIUM: SSH Session Information Leak."    
}

def extract_version(banner_text):
    """Metin içinden sadece 'Apache/'den sonra gelen versiyonu bulur."""
    
    # 1. First, we look for the word 'Apache' within the banner.
    if "Apache/" in banner_text:
        # 2. Capture the numbers and dots immediately after the word Apache/
        # Regex Explanation: Finds the Apache/ part and stores the following part (\d+\.\d+\.?\d*) in memory.
        match = re.search(r'Apache/(\d+\.\d+\.?\d*)', banner_text)
        if match:
            # By using .group(1), we extract only the number inside the parentheses (2.4.7).
            return match.group(1)
            
    return None
    

def advanced_analyze(file_path):
    """It reads the report and performs intelligent version matching."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        
        print(f"--- Advanced Analyzed started for {data['target']} ---\n")
        
        for finding in data['findings']:
            banner = finding['banner']
            port = finding['port']
            
            if banner:
                # 1. Extract the version from the text.
                version = extract_version(banner)
                
                if version:
                    print(f"[*] Port {port}: Detected version -> {version}")
                    
                    # 2. Is the extracted version available in our database?
                    if version in VULN_CATALOG:
                        print(f" [!!!] ALARM: {VULN_CATALOG[version]}")
                    else:
                        print(" [✓] There are no reported vulnerabilities for this version.")
                else:
                    print(f"[*] Port {port}: The version number could not be determined.")
    except Exception as e:
        print(f"Error Occurred: {e}")

if __name__ == "__main__":
    advanced_analyze("scan_report.json")
    