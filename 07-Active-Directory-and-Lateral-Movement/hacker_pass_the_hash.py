import time
import secrets

class PassTheHashSimulatedExploit:
    def __init__(self):
        # Sample NTLM password hashes stolen from memory (LSASS) 
        # on a compromised victim machine during a real penetration test.
        self.stolen_hashes = {
            "stg_admin": "aad3b435b51404eeaad3b435b51404ee:3dbde697d71690a769204beb12283678",
            "domain_user_1": "aad3b435b51404eeaad3b435b51404ee:51a4d13e316e64177b949ecdd3039d6d",
            "enterprise_global_admin": "aad3b435b51404eeaad3b435b51404ee:cc00551722cd15e21e64177b949ecdd"
        }
        
        # List of target computers (servers) on the network
        self.target_network_servers = ["10.10.100.5", "10.10.100.10", "10.10.100.20"]
    
    def execute_pth_attack(self, account_to_use, target_ip):
        print(f"\n[PTH EXPLOIT] Attempting Lateral Movement to {target_ip}...")
        time.sleep(0.5)
        
        # STEP 1: Check if this account is among the stolen hashes.
        if account_to_use not in self.stolen_hashes:
            print(f"[-] Error: No hash found for account: {account_to_use}")
            return False
        
        ntlm_hash = self.stolen_hashes[account_to_use]
        print(f"[*] Extracting NTLM Hash for [{account_to_use}]: {ntlm_hash}")
        
        # Step 2: Network Handshake and Challenge Simulation
        # Windows networks do not request the password when connecting to the server; instead, they send a random string (Challenge).
        # The computer encrypts this string using its stored password hash and sends it back.
        server_challange = secrets.token_hex(8) # Random 8-byte "challenge" code sent by the server
        print(f"[*] Received SMB Network Challange from target: {server_challange}")
        time.sleep(0.5)
        
        # Step 3: We sign this challenge using only the hash we have, without knowing the password!
        # This is the magic of the attack: We don't need the password; the hash suffices.
        client_response = f"AUTH_RESP_USING_HASH_{ntlm_hash[:10]}_{server_challange}"
        print(f"[+] Signed challange using stolen hash. Sending Response to target...")
        time.sleep(0.5)
        
        
        # Step 4: The target server checks. If the signature we sent is correct, it opens the door.
        if "enterprise_global_admin" in account_to_use or "admin" in account_to_use:
            print(f"🟩 [SUCCESS] Pass-to-Hash successfull! Connected to {target_ip} as SYSTEM_ADMIN!")
            print(f"🟩 [LATERAL MOVEMENT] Dropping backdoor shell on {target_ip}...")
            return True
        else:
            print(f"🟨 [LIMITED] Connected to {target_ip} but user has no Admin rights. Session limited.")
            return False

if __name__ == "__main__":
    exploit = PassTheHashSimulatedExploit()
    
    # We are launching the internal network penetration simulation
    # First, we try a low-privileged user, then we pass the full-privilege admin hash!
    exploit.execute_pth_attack(account_to_use="domain_user_1", target_ip="10.10.100.5")
    print("=" * 65)
    exploit.execute_pth_attack(account_to_use="enterprise_global_admin", target_ip="10.10.100.10")