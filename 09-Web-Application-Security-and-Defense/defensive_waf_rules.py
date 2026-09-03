import html
import re
from typing import Dict, List, Tuple

class BlueTeamWAFRuleEngine:
    """
    Defensive WAF Rule & De-obfuscation Engine.
    Normalizes obfuscated HTTP payloads (SQLİ, XSS) and inspects them against signature rules.
    """
    def __init__(self):
        # Known threat signatures (Normalized regex patterns)
        self.sqli_signatures = [
            r"union\s+select",
            r"or\s+1\s*=\s*1",
            r"select\s+.*\s+from"
        ]
        self.xss_signatures = [
            r"<script.*?>.*?</script>",
            r"alert\s*\(.*?\)",
            r"document\.cookie"
        ]
    
    def normalize_payload(self, raw_payload: str) -> str:
        """
        Step 1: Normalization Pipeline (De-obfuscation).
        Reverses attack obfuscation techniques to reveal the raw malicious intent.
        """
        normalized = raw_payload
        
        # 1. Decode HTML Entities (e.g., &#97; -> a)
        normalized = html.unescape(normalized)
        
        # 2. Remove Inline SQL Comments (replace /**/ with space)
        normalized = re.sub(r'/\*.*?\*/', ' ', normalized)
        
        # 3. Decode Hexadecimal representations (e.g., 0x61646d696e -> admin)
        def decode_hex_match(match):
            hex_str = match.group(1)
            try:
                return bytes.fromhex(hex_str).decode('utf-8', errors='ignore')
            except ValueError:
                return match.group(0)
        
        normalized = re.sub(r'0x([0-9a-fA-F]+)', decode_hex_match, normalized)
        
        # 4. Standardize Case (Lowercase everything for uniform matching)
        normalized = normalized.lower()
        
        # 5. Compress multiple spaces into a single space
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
    
    def inspect_payload(self, raw_payload: str) -> Dict:
        """
        Step 2: Payload Inspection.
        Normalizes the input and checks for SQLi and XSS signature matches.
        """
        # Run through the normalization engine
        clean_payload = self.normalize_payload(raw_payload)
        
        detected_rules: List[str] = []
        
        # Check SQLi Signatures
        for pattern in self.sqli_signatures:
            if re.search(pattern, clean_payload):
                detected_rules.append(f"SQLI_RULE_MATCH: {pattern}")
        
        # Check XSS Signatures
        for pattern in self.xss_signatures:
            if re.search(pattern, clean_payload):
                detected_rules.append(f"XSS_RULE_MATCH: {pattern}")
        
        is_blocked = len(detected_rules) > 0
        
        return {
            "is_blocked": is_blocked,
            "raw_payload": raw_payload,
            "normalized_payload": clean_payload,
            "triggered_rules": detected_rules,
            "action": "BLOCK_REQUEST (403)" if is_blocked else "ALLOW_REQUEST (200)"
        }

if __name__ == "__main__":
    from offensive_waf_bypass import RedTeamWAFBypassEngine
    
    print("==================================================")
    print(" BLUE TEAM WAF ENGINE: DE-OBFUSCATION & INSPECTION")
    print("==================================================\n")
    
    waf = BlueTeamWAFRuleEngine()
    attacker = RedTeamWAFBypassEngine()
    
    # 1. Test Obfuscated SQLi Payload
    raw_sqli = "UNION SELECT username, password FROM users WHERE id = 1 OR  1=1"
    obfuscated_sqli = attacker.obfuscate_sqli_comment_insertion(raw_sqli)
    
    sqli_report = waf.inspect_payload(obfuscated_sqli)
    
    print("[1] Inspecting Obfuscated SQLi Payload:")
    print(f" -> Incoming Payload  : {sqli_report['raw_payload']}")
    print(f" -> Normalized Payload: {sqli_report['normalized_payload']}")
    print(f" -> Triggered Rules   : {sqli_report['triggered_rules']}")
    print(f" -> WAF Action        : {sqli_report['action']}\n")

    # 2. Test Obfuscated XSS Payload
    raw_xss = "<script>alert('XSS')</script>"
    obfuscated_xss = attacker.obfuscate_xss_case_mixing(raw_xss)
    
    xss_report = waf.inspect_payload(obfuscated_xss)

    print("[2] Inspecting Obfuscated XSS Payload:")
    print(f" -> Incoming Payload  : {xss_report['raw_payload']}")
    print(f" -> Normalized Payload: {xss_report['normalized_payload']}")
    print(f" -> Triggered Rules   : {xss_report['triggered_rules']}")
    print(f" -> WAF Action        : {xss_report['action']}\n") 