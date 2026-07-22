import time
from datetime import datetime

class ASREPMonitoringEngine:
    def __init__(self, time_window_sec=5, max_attempts=2):
        self.time_window_sec = time_window_sec
        self.max_attempts = max_attempts
        # Telemetry Pool: { source_ip: [(timestamp, target_user, preauth_type, ticket_encryption)] }
        self.asrep_telemetry = {}
        self.flagged_users = set()
    
    def process_event_4768(self, source_ip, target_user, preauth_type, encryption_type):
        """Windows Event ID 4768 Log Parsers and Risk Analytics Engine."""
        current_time = time.time()
        timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n[{timestamp_str}] [SIEM] Event ID 4768 | Source: {source_ip} | Target: {target_user}")
        
        # Pre-Authentication Status Check
        # If the Preauth Type is "0" or "Disabled", it means a TGT was requested without entering a password!
        if preauth_type in [0, "Disabled", "0x0"]:
            print(f"    [SECURITY WARNING] AS-REQ received WITHOUT Pre-Authentication for user '{target_user}'!")
            
            if "RC4" in encryption_type or "0x17" in encryption_type:
                print(f" [CRITICAL ANOMALY] Weak Encryption Requested ({encryption_type}). High probability of AS-REP Roasting attack!")
                
                # Telemetry Log
                if source_ip not in self.asrep_telemetry:
                    self.asrep_telemetry[source_ip] = []
                
                self.asrep_telemetry[source_ip].append((current_time, target_user, encryption_type))
                
                # Sliding Window Cleanup (Retains the last X seconds)
                self.asrep_telemetry[source_ip] = [
                    event for event in self.asrep_telemetry[source_ip]
                    if current_time - event[0] <= self.time_window_sec
                ]
                
                recent_count = len(self.asrep_telemetry[source_ip])
                print(f"[AUDIT] Active Pre-Auth-Disabled AS-REQs from {source_ip} in last {self.time_window_sec}s: {recent_count}")
                
                if recent_count >= self.max_attempts:
                    self.trigger_soc_incident(source_ip, target_user)
        else:
            print(f"[INFO] Standart Kerberos Pre-Auth verified for '{target_user}'. Request legitimized")
    
    def trigger_soc_incident(self, source_ip, compromised_user):
        print(f"\n🚨🚨🚨 [SOC INCIDENT RESPONSE ALERT] AS-REP ROASTING PATTERN DETECTED! 🚨🚨🚨")
        print(f"    [ATTACK VECTOR] Bulk AS-REQ requests bypassing Pre-Authentication.")
        print(f"    [OFFENDING IP] {source_ip}")
        print(f"    [TARGET USER] {compromised_user}")
        print(f"    [MITIGATION] Enforcing Active Directory GPO: Re-enabling Pre-Authentication for target account.")
        print(f"    [ACTION] Null-routing IP {source_ip} on Perimeter Firewall.")
        self.flagged_users.add(compromised_user)

if __name__ == "__main__":
    siem = ASREPMonitoringEngine(time_window_sec=5, max_attempts=2)

    # Normal / Safe User Request
    siem.process_event_4768("10.10.20.15", "j.doe", preauth_type=2, encryption_type="AES256-CTS-HMAC-SHA1-96")
    time.sleep(1)

    # Suspicious AS-REP Roasting Attack Traffic
    siem.process_event_4768("10.10.20.88", "svc_scanner", preauth_type=0, encryption_type="RC4-HMAC")
    time.sleep(0.5)
    siem.process_event_4768("10.10.20.88", "legacy_admin", preauth_type=0, encryption_type="RC4-HMAC")
                