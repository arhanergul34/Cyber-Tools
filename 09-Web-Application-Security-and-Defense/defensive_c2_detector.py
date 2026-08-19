import json
import base64
import math
from typing import Dict, Tuple

class BlueTeamC2Detector:
    def __init__(self, entropy_threshold: float = 5.5):
        self.entropy_threshold = entropy_threshold
        self.suspicious_events = []
    
    def calculate_entropy(self, data_bytes: bytes) -> float:
        if not data_bytes:
            return 0.0
        
        byte_counts = {}
        for b in data_bytes:
            byte_counts[b] = byte_counts.get(b, 0) + 1
        
        entropy = 0.0
        length = len(data_bytes)
        for count in byte_counts.values():
            probability = count / length
            entropy -= probability * math.log2(probability)
        
        return entropy
    
    def inspect_packet(self, packet_raw: str) -> Tuple[bool, Dict]:
        try:
            payload = json.loads(packet_raw)
        except json.JSONDecodeError:
            return False, {"reason": "Not a valid JSON format"}
        
        if "nonce" not in payload or "ciphertext" not in payload:
            return False, {"reason": "Base64 decoding failed"}
        
        try:
            nonce_bytes = base64.b64decode(payload["nonce"])
            ciphertext_bytes = base64.b64decode(payload["ciphertext"])
        except Exception:
            return False, {"reason": "Base64 decoding failed"}
        
        nonce_len = len(nonce_bytes)
        ciphertext_entropy = self.calculate_entropy(ciphertext_bytes)
        
        is_suspicious = False
        findings ={
            "nonce_bytes_len": nonce_len,
            "ciphertext_entropy": round(ciphertext_entropy, 4),
            "threat_detected": False
        }
        
        if nonce_len == 12 and ciphertext_entropy > self.entropy_threshold:
            is_suspicious = True
            findings["threat_detected"] = True
            findings["signature"] = "SUSPICIOUS_AES_GCM_C2_CHANNEL"
            
            self.suspicious_events.append(findings)
        
        return is_suspicious, findings
    
    def attempt_break_or_validate(self, packet_raw: str, candidate_passphrase: str, salt: bytes) -> Tuple[bool, str]:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes
        
        try:
            payload = json.loads(packet_raw)
            nonce = base64.b64decode(payload["nonce"])
            ciphertext = base64.b64decode(payload["ciphertext"])
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100_000
            )
            key = kdf.derive(candidate_passphrase.encode('utf-8'))
            cipher = AESGCM(key)
            
            decrypted_bytes = cipher.decrypt(nonce, ciphertext, associated_data=None)
            return True, decrypted_bytes.decode('utf-8')
        except Exception:
            return False, "Decryption /Integrity Chech Failed"
        