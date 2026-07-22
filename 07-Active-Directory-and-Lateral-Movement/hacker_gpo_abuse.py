import time
import secrets
from datetime import datetime

class GPOAbuseSimulator:
    def __init__(self):
        self.domain = "CORP.LOCAL"
        self.sysvol_path = f"\\\\{self.domain}\\SYSVOL\\{self.domain}\\Policies"
        # Target GPO Object (e.g., Default Domain Policy GUID)
        self.target_gpo_guid = "{31B2F340-016D-11D2-945F-00C04FB984F9}"
        
        # Vulnerable ACL Status (Write permission granted to the Domain Users group)
        self.gpo_permissions = {
            self.target_gpo_guid: {
                "name": "Default Domain Policy",
                "write_access_groups": ["Domain Admins", "Domain Users"] # Vulnerability!
            }
        }
    
    def simulate_gpo_injection(self, attacker_user):
        print(f"[{datetime.now().strftime('%T')}] [RED TEAM] Initializing GPO Abusing & Persistence Module...")
        print(f"[*] Target SYSVOL Path: {self.sysvol_path}")
        time.sleep(1.0)
        
        gpo_info = self.gpo_permissions.get(self.target_gpo_guid)
        print(f"\n[*] Auditing ACL Permissions for GPO: {gpo_info['name']} ({self.target_gpo_guid})")
        
        if "Domain Users" in gpo_info["write_access_groups"]:
            print(f"    [!] VULNERABILITY CONFIRMED: Over-privileged ACL detected!")
            print(f"    [!] User '{attacker_user}' has write permissions on Policy Files.")
            time.sleep(0.8)
            
            # Malicious Scheduled Task XML Injection Simulation
            malicious_task_xml = f"""
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Actions Context="Author">
    <Exec>
      <Command>powershell.exe</Command>
      <Arguments>-nop -w hidden -enc aXdleG9yY2FsbGJhY2s...</Arguments>
    </Exec>
  </Actions>
</Task>
            """.strip()
            
            print(f"    [*] Injecting malicious Scheduled Task into SYSVOL Policy ScheduledTasks.xml...")
            time.sleep(1.0)
            print(f"    [+] [GPO MODIFIED] Malicious payload successfully written to SYSVOL!")
            print(f"🟩 [EXPLOIT SUCCESS] Immediate/Next-Reboot persistence established across domain endpoints.")
        else:
            print(f"    [-] Access Denied: GPO ACLs strictly enforced for '{attacker_user}'.")

if __name__ == "__main__":
    attacker = GPOAbuseSimulator()
    attacker.simulate_gpo_injection(attacker_user="j.doe")
    
            
                   