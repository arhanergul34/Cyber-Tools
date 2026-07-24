import time
from datetime import datetime

class DCSyncMitigationEngine:
    def __init__(self):
        # Legitimate Domain Controller IP and Account List (Whitelist)
        self.authorized_dcs = {
            "10.10.10.10": "CORP\\DC01$",
            "10.10.10.11": "CORP\\DC02$"
        }
        self.dcsync_right_guid = "1131f6ad-9c0e-11d1-f79f-00c04fc2dcd2"
    
    def inspect_rpc_replication_event(self, source_ip, requesting_user, requested_guid):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"\n[{timestamp}] [SIEM TELEMETRY] Inspecting Event 4662 | Source IP: {source_ip} | User: {requesting_user}")
        
        # Stage 1: Replication GUID Check
        if requested_guid == self.dcsync_right_guid:
            # Stage 2: Is the source making the request a legitimate DC?
            if source_ip not in self.authorized_dcs or requesting_user != self.authorized_dcs.get(source_ip):
                print(f"🚨 [CRITICAL ALARM] DCSYNC ATTACK IN PROGRESS DETECTED!")
                print(f"    [VIOLATION] Non-DC Account '{requesting_user}' requested full NTDS Replication!")
                self.trigger_automated_mitigation(source_ip, requesting_user)
            else:
                print(f"[+] Legitimate DC replication request verified for {requesting_user}.")
    
    def trigger_automated_mitigation(self, source_ip, offending_user):
        print("\n" + "🛡️ " * 15 + " SOAR AUTOMATED RESPONSE " + "🛡️ " * 15)
        print(f" 1. REVOKING ACL : Stripping 'DS-Replication-Get-Changes-All' from {offending_user}")
        print(f" 2. BLOCKING IP  : Adding {source_ip} to Host Isolation Firewall Rule")
        print(f" 3. KICK SESSIONS: Terminating active Kerberos TGT/TGS tickets for {offending_user}")
        print(f" 4. ROTATE KRBTGT: Triggering automated krbtgt password reset workflow")
        print("=" * 75)

if __name__ == "__main__":
    defender = DCSyncMitigationEngine()
    
    # The Moment SIEM Captures the Log Triggered by the Attack Code
    defender.inspect_rpc_replication_event(
        source_ip="10.10.20.88",
        requesting_user="CORP\\svc_backup_mgr",
        requested_guid="1131f6ad-9c0e-11d1-f79f-00c04fc2dcd2"
    )