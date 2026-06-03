import base64
import os

class SourceCodeObfuscator:
    def __init__(self, source_file_path, output_file_path):
        self.source_file_path = source_file_path
        self.output_file_path = output_file_path
        
    def obfuscate(self):
        print(f"[*] Intellectual Property Protection (IPP) active.")
        print(f"[*] Target file to encrypt: {self.source_file_path}")
        print("=" * 75) 
        
        if not os.path.exists(self.source_file_path):
            print(f"[-] Error: Source file '{self.source_file_path}' not found.")
            return
        
        try:
            # Step 1: Read the original clean code
            with open(self.source_file_path, "r", encoding="utf-8") as file:
                original_code = file.read()
            
            print("[*] Reading source code and converting to binary matrix...")
            
            # Step 2: Convert the code from string to byte format (Required for encryption!)
            code_bytes = original_code.encode("utf-8")
            
            # Step 3: Obfuscate the code using the Base64 cyber encryption algorithm.
            obfuscated_bytes = base64.b64encode(code_bytes)
            
            # Step 4: Convert the encrypted bytes back to text
            obfuscated_string = obfuscated_bytes.decode("utf-8")
            
            # Step 5: Creating a Cyber ​​Capsule!
            # We are preparing a shell in which Python will secretly decrypt ('exec') and execute the encrypted code in the background.
            payload = f"import base64\nexec(base64.b64decode('{obfuscated_string}').decode('utf-8'))"
            
            # Step 6: Seal the new obfuscated cyber code into the file.
            with open(self.output_file_path, "w", encoding="utf-8") as file:
                file.write(payload)
            
            print(f"[+] Obfuscation successfully completed!")
            print(f"[+] Protected output saved to: {self.output_file_path}")
            print(f"[-] Security Note: Human-readability has been destroyed. Execution logic preserved.")
            print("=" * 75)
        
        except Exception as e:
            print(f"[-] Obfuscation failed due to error: {e}")

if __name__ == "__main__":
    # For testing purposes: We will target and encrypt our first project, 'static_code_analyzer.py'!
    obfuscator = SourceCodeObfuscator(
        source_file_path="static_code_analyzer.py",
        output_file_path="protected_analyzer.py"
    )
    obfuscator.obfuscate()
        