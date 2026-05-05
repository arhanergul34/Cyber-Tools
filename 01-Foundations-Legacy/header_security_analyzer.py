import json

# STEP 1: Security Checklist
# These headings MUST be on a website.
REQUIRED_HEADERS = {
    "X-Frame-Options": "It provides protection against Clickjacking.",
    "X-XSS-Protection": "It prevents Cross-Site Scripting (XSS) attacks.",
    "Content-Security-Policy": "Modern browser firewall (CSP).",
    "Strict-Transport-Security": "It forces the connection to use HTTPS (HSTS)."  
}

def analyze_headers(file_path):
    """It reads the report and checks for missing critical security headings."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        
        print(f"--- Security Header Analysis for {data['target']} ---\n")
        
        for finding in data['findings']:
            banner = finding['banner']
            port = finding['port']
            
            #Let's analyze only the web ports (80, 443).
            if port in [80, 443] and banner:
                print(f"[*] Port {port} is Being Analyzed...")
                
                # A loop to find missing headings
                missing_headers = []
                for header, description in REQUIRED_HEADERS.items():
                    # If the title name (e.g., X-Frame-Options) does NOT appear in the banner
                    if header not in banner:
                        missing_headers.append(f"{header} ({description})")
                
                # Print results to screen
                if missing_headers:
                    print(f" [!] CRITICAL DEFICIENCIES HAVE BEEN IDENTIFIED:")
                    for h in missing_headers:
                        print(f"     -{h}")
                else:
                    print(" [✓] All basic safety topics are covered. Well done!")
                print("-" * 30)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    analyze_headers("scan_report.json")           