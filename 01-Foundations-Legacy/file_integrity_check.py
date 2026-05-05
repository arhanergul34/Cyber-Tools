import hashlib # To obtain the file fingerprint (hash)
import os
from logger_tool import log_event

def get_file_hash(file_path):
    """Calculates the unique fingerprint (SHA256) of a file."""
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Read the file in parts (to prevent large files from straining memory)
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None
    
def check_integrity(file_to_watch, original_hash):
    """It compares the current version of the file with the original fingerprint."""
    current_hash = get_file_hash(file_to_watch)
    
    if current_hash is None:
        log_event(f"ERROR: {file_to_watch} not found!", "error")
        return
    
    if current_hash == original_hash:
        log_event(f"[✓] SAFE: No changes to {file_to_watch}.", "info")
    else:
        log_event(f"[!] WARNING: {file_to_watch} MODIFIED! May be leaked!", "warning")
        print(f"Old Hash: {original_hash}")
        print(f"New Hash: {current_hash}")
        
# Example Usage
if __name__ == "__main__":
    # Choose a file name for the test
    test_file = "targets.txt"
    
    # Step 1: Fingerprint the "clean" version of the file.
    print(f"--- {test_file} Starting to Watch ---")
    clean_hash = get_file_hash(test_file)
    print(f"Original Fingerprint: {clean_hash}")
    
    # Step 2: Check
    check_integrity(test_file, clean_hash)

