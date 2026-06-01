import hashlib
import time
import os

class HashIntegrityVerifier:
    def __init__(self, target_file_path):
        self.target_file_path = target_file_path
        # The box where we will store the file's initial secure fingerprint
        self.original_hash = None
        
    def calculate_file_hash(self):
        """Calculates the unique SHA-256 fingerprint of the target file."""
        sha256_hasher = hashlib.sha256()
        try:
            # We are opening the file in binary read mode ('rb') (so that it works regardless of whether the content is an image, code, or text).
            with open(self.target_file_path, "rb") as file:
                # We read in 4KB chunks to prevent RAM bloat when handling large files.
                for chunk in iter(lambda: file.read(4096), b""):
                    sha256_hasher.update(chunk)
            return sha256_hasher.hexdigest()
        
        except FileNotFoundError:
            return None
    
    def monitor_integrity(self, interval_second=5):
        print(f"[*] Integrity Monitoring started for: {self.target_file_path}")
        
        # Upon initial startup, we capture the fingerprint of the file's clean/original state.
        self.original_hash = self.calculate_file_hash()
        
        if not self.original_hash:
            print(f"[-] Error: Target file '{self.target_file_path}' not found. Monitoring aborted.")
            return
        
        print(f"[*] Legitimate File Signature baseline established:")
        print(f"[-] SHA-256: {self.original_hash}")
        print("[*] Monitoring system is active. Watching for unauthorized alterations... (Press Ctrl+C to stop)")
        print("-" * 75)
        
        try:
            while True:
                # Check the file again every specified number of seconds (e.g., every 5 seconds).
                time.sleep(interval_second)
                current_hash = self.calculate_file_hash()
                
                # Scenario A: If the file was deleted by a malicious hacker
                if current_hash is None:
                    print(f"\n[🚨 CRITICAL INTEGRITY ALERT] Target File '{self.target_file_path}' HAS BEEN DELETED!")
                    break
                
                # Scenario B: If the file content has been modified (If the fingerprints do not match!)
                elif current_hash != self.original_hash:
                    print(f"\n[🚨 CRITICAL INTEGRITY ALERT] Unauthorized Modification Detected!")
                    print(f"[-] Original Hash: {self.original_hash}")
                    print(f"[-] Corrupted Hash: {current_hash}")
                    print(f"[-] Security Note: File tampering detected! Immediate incident response required.")
                    print("-" * 75)
                    # After triggering the alarm, we can either approve the new hash to break the loop or continue monitoring.
                    # We are leaving the lock open so that the alarm continues to sound until an analyst observes the situation and intervenes.
                    self.original_hash = current_hash
                
        except KeyboardInterrupt:
            print("\n[*] Integrity Monitoring system shut down gracefully.")

if __name__ == "__main__":
    # Let's protect the file from our previous project for testing purposes!
    verifier = HashIntegrityVerifier(target_file_path="regex_pii_detector.py")
    verifier.monitor_integrity(interval_second=3)
            