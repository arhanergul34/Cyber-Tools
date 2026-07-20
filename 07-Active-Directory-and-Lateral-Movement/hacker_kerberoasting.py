import time
import hashlib
import secrets
from datetime import datetime, timedelta

class AdvancedKerberoastingSimulator:
    def __init__(self):
        # Realistic Active Directory SPN and Service Accounts Database
        self.domain_controllers = ["DC01.corp.local", "DC02.corp.local"]
        self.target_spns = {
            "MSSQLSvc/sql-prod.corp.local:1433": {"sam_account": "sql_svc", "enc_type": "RC4-HMAC"},
            "http/web-internal.corp.local": {"sam_account": "web_svc", "enc_type": "AES256-CTS-HMAC-SHA1-96"},
            "HOST/backup-dc.corp.local": {"sam_account": "krbtgt", "enc_type": "AES256-CTS-HMAC-SHA1-96"}
        }
    
    def craft_mock_tgs_hash(self, sam_account, enc_type):
        """Generates a hash in a format that the attacker can feed into hash-cracking tools (Hashcat/John)."""
        salt = secrets.token_hex(8)
        dummy_hash = hashlib.sha256(sam_account.encode() + salt.encode()).hexdigest()
        
        if enc_type == "RC-4-HMAC":
            return f"$krb5tgs$23$*{sam_account}*CORP.LOCAL*hashes*:{dummy_hash[:32]}"
        else:
            return f"$krb5tgs$18$*{sam_account}*CORP.LOCAL*hashes*:{dummy_hash[:64]}"
    
    def execute_bulk_roasting(self):
        print(f"[{datetime.now().strftime('%T')}] [RED TEAM] Initializing Kerberoasting Automation Framework...")
        print(f"[*] Querying Domain Controllers {self.domain_controllers} for SPN registirations...")
        time.sleep(1.0)
        
        extracted_tickets = []
        for spn, info in self.target_spns.items():
            print(f"\n[*] Sending TGS-REQ (Ticket Granting Service Request) for: {spn}")
            print(f"    [-] Target Account: {info['sam_account']}")
            print(f"    [-] Requested Encrpytion: {info['enc_type']}")
            time.sleep(0.8) # Network latency simulation
            
            # Ticket structure simulation
            ticket_id = secrets.token_hex(4).upper()
            expriy = (datetime.now() + timedelta(hours=10)).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"[+] [TGS-REP Received] Ticket ID: TGS-{ticket_id} | Valid Until: {expriy}")
            tgs_hash = self.craft_mock_tgs_hash(info['sam_account'], info['enc_type'])
            print(f"🟩 [EXPLOIT] Successfully extracted crackable ticket hash:")
            print(f"    {tgs_hash}")
            
            extracted_tickets.append({"spn":spn, "hash": tgs_hash})
        
        print("\n" + "="*80)
        print(f"[{datetime.now().strftime('%T')}] [SUCCESS] Kerboroasting completed. Total hashes dumped: {len(extracted_tickets)}")
        print("="*80)

if __name__ == "__main__":
    roaster = AdvancedKerberoastingSimulator()
    roaster.execute_bulk_roasting()
                