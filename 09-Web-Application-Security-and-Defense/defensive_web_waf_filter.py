import re
import html
import time
import json
from urllib.parse import unquote

class AdvancedWebWAFEngine:
    """
    Enterprise Defensive Web Application Firewall (WAF) & Security Engine.
    Features:
    - Multi-Layer Attack Inspection (SQLİ, XSS, Path Traversal, Command Injection)
    - Input Sanitization & HTML Encoding Engine
    - Sliding-Window Rate Limiting Engine (Anti-Brute Force / DoS)
    - Dynamic IP Blacklisting / Blocking Engine
    - SIEM-Ready JSON Security Event Logging
    """
    def __init__(self, max_requests_per_window=3, window_seconds=10):
        # Security Rules Database
        self.rules = {
            "SQL Injection": [
                r"(?i)(\%27|\'|\-\-|\%23|#)",
                r"(?i)\b(UNION|SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|EXEC|SLEEP)\b",
                r"(?i)OR\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?"
            ],
            "Cross-Site Scripting (XSS)": [
                r"(?i)<script.*?>.*?</script>",
                r"(?i)javascript\s*:",
                r"(?i)oneerror\s*=",
                r"(?i)onload\s*=",
                r"(?i)<svg.*?>"
            ],
            "Path Traversal": [
                r"\.\./",
                r"\.\.\\",
                r"(?i)/etc/passwd",
                r"(?i)c:\\boot.ini"
            ],
            "OS Command Injection": [
                r"(?i);|&&|\|\|",
                r"(?i)\b(cat|ls|whoami|nc|bash|cmd|powershell)\b"
            ]
        }
        
        # Rate Limiting Configuration
        self.max_requests = max_requests_per_window
        self.window_seconds = window_seconds
        self.request_history = {}
        self.blacklisted_ips = set()
    
    def _is_rate_limited(self, client_ip):
        """It monitors IP-based request limit violations using the sliding window rate-limiting algorithm."""
        current_time = time.time()
        if client_ip not in self.request_history:
            self.request_history[client_ip] = [
                t for t in self.request_history[client_ip] if current_time - t <= self.window_seconds  
            ]
            
            self.request_history[client_ip].append(current_time)
            
            if len(self.request_history[client_ip]) > self.max_requests:
                self.blacklisted_ips.add(client_ip)
                return True
            return False
    
    def sanitize_input(self, user_input):
        """It neutralizes XSS by converting harmful characters into HTML entities."""
        decoded_input = unquote(user_input)
        return html.escape(decoded_input)
    
    def log_security_event(self, client_ip, param_name, param_value, attack_type, matched_rule):
        """Generates security logs in JSON format suitable for transmission to SIEM systems."""
        event = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "client_ip": client_ip,
            "parameter": param_name,
            "raw_value": param_value,
            "attack_category": attack_type,
            "matched_pattern": matched_rule,
            "action_taken": "BLOCKED_HTTP_403"
        }
        print(f"[LOG SIEM EVENT]: {json.dumps(event)}")
    
    def inspect_request(self, client_ip, param_name, param_value):
        """
        Subjects the incoming HTTP request to IP checking, rate limiting, and rule scanning.
        """
        # 1. IP Blacklist Check
        if client_ip in self.blacklisted_ips:
            print(f"[🚨 WAF DROP] IP [{client_ip}] is BLACKLISTED. Request Rejected immediately.")
            return False, "BLACK_LISTED"
        
        # 2. Rate Limiting (Excessive Request) Control
        if self._is_rate_limited(client_ip):
            print(f"[WAF BLOCK] Rate Limit Exceeded for IP [{client_ip}]! Auto-Blacklisting applied.")
            return False, "RATE_LIMIT_EXCEEDED"
        
        # 3. Rule-Based Payload Scanning
        decoded_value = unquote(param_value)
        for attack_type, patterns in self.rules.items():
            for pattern in patterns:
                if re.search(pattern, decoded_value):
                    print(f"\n[🚨 WAF BLOCK] Threat Detected!")
                    print(f" ├─ Client IP      : {client_ip}")
                    print(f" ├─ Parameter      : {param_name}")
                    print(f" ├─ Attack Type    : {attack_type}")
                    print(f" └─ Matched Rule   : {pattern}")
                    
                    self.log_security_event(client_ip, param_name, param_value, attack_type, pattern)
                    return False, attack_type
        
        return True, "CLEAN"

if __name__ == "__main__":
    waf = AdvancedWebWAFEngine(max_requests_per_window=3, window_seconds=10)
    
    print("==================================================")
    print(" ADVANCED DEFENSIVE WAF & SECURITY ENGINE")
    print("==================================================\n")
    
    test_ip = "192.168.1.105"
    
    # 1. Scenario: Analysis of Various Attack Vectors
    scenarios = [
        ("search", "laptop"),
        ("id", "1' OR 1=1--"),
        ("comment", "<script>alert('xss')</script>"),
        ("file", "../../etc/passwd"),
        ("cmd", "127.0.0.1; whoami")
    ]
    
    print("--- SCENARIO 1: PAYLOAD INSPECTION ---")
    for param, val in scenarios:
        is_safe, status = waf.inspect_request(test_ip, param, val)
        if is_safe:
            clean_val = waf.sanitize_input(val)
            print(f"[PASSED] Input Safe. Sanitized: {clean_val}\n")
        else:
            print(f"[HTTP 403] Forbidden Request Payload.\n")
    
    # Scenario 2: DoS / Rate Limit Blocking Simulation
    print("--- SCENARIO 2: RATE LIMITING & AUTOMATIC BLACKLISTING ---")
    spammer_ip = "10.0.0.50"
    for i in range(5):
        print(f"Attempt #{i+i} from IP {spammer_ip}:")
        is_safe, status = waf.inspect_request(spammer_ip, "item", "normal_product")
        if not is_safe:
            print(f"[BLOCKED] Action Status: {status}\n")
        else:
            print(f"[PASSED] Request Allowed.\n")
            
        
        