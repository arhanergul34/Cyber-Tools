import time
from datetime import datetime

class PassTheHashMonitoringEngine:
    def __init__(self):
        # High-risk admin accounts
        self.sensitive_accounts = ["CORP\\Administrator", "Administrator", "CORP\\Domain Admins"]
    
    def process_event_4624_and_7045(self, source_ip, user_name, logon_type, auth_package, key_length, service_name=None):
        """
        Event ID 4624: Successful Logon (Type 3 = Network)
        Event ID 7045: A service was installed in the system
        """
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"\n[{timestamp}] [SIEM TELEMETRY] Analyzing Network Activity | Source: {source_ip} | User: {user_name}")
        
        is_pth_detected = False
        
        # 1. Criterion: Network Logon (Type 3) and NTLM Authentication
        if logon_type == 3 and auth_package.upper() == "NTLM":
            # 2. Criterion: Sensitive/High-Privilege Account Review
            if user_name in self.sensitive_accounts:
                # Criterion 3: Suspicious Service Creation (PsExec / Indicator of Lateral Movement)
                if service_name:
                    print(f"🚨 [CRITICAL ALERT] PASS-THE-HASH (PtH) LATERAL MOVEMENT DETECTED!")
                    print(f"    [INDICATOR 1] Logon Type 3 (Network) via NTLM Authentication")
                    print(f"    [INDICATOR 2] High-Privilege Account Context: {user_name}")
                    print(f"    [INDICATOR 3] Suspicious Service Execution: '{service_name}'")
                    is_pth_detected = True
                    self.trigger_mitigation(source_ip, user_name, service_name)
        
        if not is_pth_detected:
            print(f"[+] Activity verified as standard network authentication.")
    
    def trigger_mitigation(self, source_ip, user_name, service_name):
        print("\n" + "🛡️ " * 15 + " AUTOMATED CONTAINMENT " + "🛡️ " * 15)
        print(f" 1. TERMINATE SERVICE : Stopping and removing malicious service '{service_name}'")
        print(f" 2. BLOCK NETWORK     : Isolating source IP {source_ip} on host firewall")
        print(f" 3. KILL SESSIONS     : Invalidating active NTLM/Kerberos tokens for {user_name}")
        print("=" * 75)

if __name__ == "__main__":
    defender = PassTheHashMonitoringEngine()
    
    # SIEM Log Triggered by a PtH Attack
    defender.process_event_4624_and_7045(
        source_ip="10.10.20.105",
        user_name="CORP\\Administrator",
        logon_type=3,
        auth_package="NTLM",
        key_length=128,
        service_name="PSEXEC-SVC"
    )