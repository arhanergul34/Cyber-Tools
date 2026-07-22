import time
from datetime import datetime

class GPOMonitoringEngine:
    def __init__(self):
        self.critical_gpos = ["{31B2F340-016D-11D2-945F-00C04FB984F9}"]
        self.authorized_admins = ["admin_alice", "svc_gpo_deployer"]
    
    def process_event_5136(self, source_ip, user_name, gpo_guid, modified_attribute, new_value):
        """Windows Event ID 5136 Log Parser and GPO Integrity Checker."""
        timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n[{timestamp_str}] [SIEM] Event ID 5136 | Source: {source_ip} | User: {user_name}")
        print(f"[*] Object Modified: {gpo_guid} | Attribute: {modified_attribute}")
        
        # Suspicious User Check
        if user_name not in self.authorized_admins:
            print(f"⚠️   [SECURITY ALERT] Unauthorized GPO Modification Attempt Detected by '{user_name}'!")
            
            # Critical Attribute Change Monitoring (gPCFileSysPath, ScheduledTasks, Script Injections)
            if "ScheduledTasks" in new_value or "Script" in new_value or "gPCFileSysPath" in modified_attribute:
                print(f"🚨 [CRITICAL ANOMALY] Malicious Persistence/Payload Pattern Detected in GPO Update!")
                self.trigger_gpo_incident(source_ip, user_name, gpo_guid)
        else:
            print(f"[INFO] Authorized administrative GPO change verified for '{user_name}'. Change logged.")
    
    def trigger_gpo_incident(self, source_ip, offending_user, gpo_guid):
        print(f"\n🚨🚨🚨 [SOC INCIDENT RESPONSE ALERT] SUSPICIOUS GPO MODIFICATION DETECTED! 🚨🚨🚨")
        print(f"    [ATTACK VECTOR] Malicious GPO Modification / SYSVOL Injection.")
        print(f"    [OFFENDING USER] {offending_user}")
        print(f"    [SOURCE IP] {source_ip}")
        print(f"    [TARGET GPO GUID] {gpo_guid}")
        print(f"    [MITIGATION] Reverting GPO to last known secure backup state.")
        print(f"    [ACTION] Revoking write permissions for user '{offending_user}' and isolating endpoint IP {source_ip}.")      

if __name__ == "__main__":
    siem = GPOMonitoringEngine()
    
    # Standard Change from Authorized Manager
    siem.process_event_5136("10.10.10.5", "admin_alice", "{31B2F340-016D-11D2-945F-00C04FB984F9}", "displayName", "Default Domain Policy V2")
    time.sleep(1)
    
    # GPO Change from Suspicious/Unauthorized User (Malicious Script/Task)
    siem.process_event_5136("10.10.20.99", "j.doe", "{31B2F340-016D-11D2-945F-00C04FB984F9}", "gPCFileSysPath", "\\SYSVOL\\ScheduledTasks.xml (powershell.exe)")