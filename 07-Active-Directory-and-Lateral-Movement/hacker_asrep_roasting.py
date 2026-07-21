import time
import hashlib
import secrets
from datetime import datetime

class ASREPRoastingSimulator:
    def __init__(self):
        self.domain = "CORP.LOCAL"
        self.domain_controllers = ["DC01.corp.local", "DC02.corp.local"]
        # Users in the AD Database and userAccountControl (UAC) Flags
        # 0x10000 = DONT_REQ_PREAUTH (Kerberos Pre-Auth Disabled)
        self.ad_user_database = {
            "j.doe": {"uac_flags": 0x0200, "preauth_required": True},       # Normal User
            "svc_scanner": {"uac_flags": 0x10200, "preauth_required": False}, # Vulnerable Account!
            "a.smith": {"uac_flags": 0x0200, "preauth_required": True},     # Normal User
            "legacy_admin": {"uac_flags": 0x10200, "preauth_required": False} # Vulnerable Account!
        }
    
    def craft_asrep_hash(self, username):
        """Hashcat mode 18200 generates a ticket hash in the ($krb5asrep$23$) format."""
        salt = secrets.token_hex(8)
        dummy_data = hashlib.sha256(username.encode() + salt.encode()).hexdigest()
        checksum = dummy_data[:32]
        encrypted_part = dummy_data[32:]
        return f"$krb5asrep$23${username}@{self.domain}:{checksum}${encrypted_part}"
    
    def audit_and_roast(self):
        print(f"[{datetime.now().strftime('%T')}] [RED TEAM] Initializing AS-REP Roasting Discovery Framework...")
        print(f"[*] Querying Domain Controllers {self.domain_controllers} for UAC Flag: DONT_REQ_PREAUTH (0x10000)...")
        time.sleep(1.0)
        
        vulnerable_accounts = []
        for user, data in self.ad_user_database.items():
            print(f"\n[*] Evaluating User Context: {user}@{self.domain}")
            
            if not data["preauth_required"]:
                print(f"    [!] UAC Match: DONT_REQ_PREAUTH is ENABLED for {user}!")
                print(f"    [*] Crafting AS-REQ (Authentication Service Request) without Pre-Authentication timestamp...")
                time.sleep(0.8)
                
                asrep_hash = self.craft_asrep_hash(user)
                print(f"    [+] [AS-REP Received] Pre-Auth bypass successful! Extracted AS-REP encrypted Ticket.")
                print(f"🟩 [EXPLOIT] Offline Crackable Hash Generated:")
                print(f"    {asrep_hash}")
                
                vulnerable_accounts.append({"user": user, "hash": asrep_hash})
            else:
                print(f"    [-] Account secure: Pre-Authentication is strictly enforced (KRB_ERROR: KDC_ERR_PREAUTH_REQUIRED).")
        
        print("\n" + "="*80)
        print(f"[{datetime.now().strftime('%T')}] [SUCCESS] AS-REP Roasting Completed. Total Hash Blobs Harvested: {len(vulnerable_accounts)}")
        print("="*80)

if __name__ == "__main__":
    roaster = ASREPRoastingSimulator()
    roaster.audit_and_roast()        
    