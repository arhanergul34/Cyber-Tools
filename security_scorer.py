import json

def calculate_security_score(file_path):
    """Calculates a security score out of 100 based on the system's vulnerabilities."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        
        # Our starting score is 100 (Assuming a perfectly clean system)
        score = 100
        penalties = [] # We will write here why we deducted points.

        print(f"--- {data['target']} Security Scoring Begins ---\n")
        
        for finding in data['findings']:
            banner = finding['banner']
            
            if not banner or banner == "No Banner":
                continue # We can't analyze if there's no banner, we'll skip it.
            
            # 1. CHECK: Critical Vulnerability (e.g., Apache 2.4.7)
            if "Apache/2.4.7" in banner:
                score -= 40
                penalties.append("Critical Vulnerability (Apache 2.4.7): -40 Points")
            
            # 2. CHECK: Missing Safety Headers
            required_headers = ["X-Frame-Options", "X-XSS-Protection", "Content-Security-Policy"]
            for header in required_headers:
                if header not in banner:
                    score -= 10
                    penalties.append(f"Missing Security Header ({header}): -10 Points")
        
        # Let's prevent the score from dropping below 0.
        score = max(0, score)
        
        # FINAL REPORT
        print(f"RESULT:")
        print(f"Security Score: {score} / 100") 
        
        if penalties:
            print("\nPoints are deducted for certain points:")
            for p in penalties:
                print(f" [!] {p}")
        
        # Risk Level Determination
        if score > 80:
            print("\nRisk Level: LOW (Safe)")
        elif score > 50:
            print("n\nRisk Level: MİD (Attention Should Be Paid)")
        else:
            print("\nRisk Level: HİGH (Immediate intervention is required!)")
            
    except Exception as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    calculate_security_score("scan_report.json")