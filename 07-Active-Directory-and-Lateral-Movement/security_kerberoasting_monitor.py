import time
from datetime import datetime

class EnterpriseKerberosAuditor:
    def __init__(self, time_window_sec=5, max_requests=2):
        self.time_window_sec = time_window_sec
        self.max_requests = max_requests
        # Structure: { source_ip: [(timestamp, requested_spn, encryption_type)] }
        self.ticket_log_talametry = {}
        self.isolated_ips = set()
    
    def process_event_4769(self, source_ip, account_name, requested_spn, encryption_type):
        """Windows SIEM / Event Log (ID 4769) Parsers Analysis Mechanism."""
        current_time = time.time()
        readable_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n[{readable_time}] [SIEM-LOG] Event ID 4769 | Source: {source_ip} | Account: {account_name}")
        
        if source_ip in self.isolated_ips:
            print(f"🛑 [DROP] Request from {source_ip} blocked automatically. Host it isolated.")
            return
        
        # Weak Encryption Detection (Indicates an RC4 Attack)
        if "RC4" in encryption_type:
            print(f"⚠️ [WARNING] Downgrade / Weak Encryption Detected: {encryption_type} requested for {requested_spn}!")
        
        # Update the history log window for the relevant IP address.
        if source_ip not in self.ticket_log_talametry:
            self.ticket_log_talametry[source_ip] = []
        
        self.ticket_log_talametry[source_ip].append((current_time, requested_spn, encryption_type))
        
        # Clean up old logs outside the time window (Sliding Window)
        self.ticket_log_talametry[source_ip] = [
            req for req in self.ticket_log_talametry[source_ip]
            if current_time - req[0] <= self.time_window_sec
        ]
        
        # Threshold Check (Anomaly / UBA Detection)
        recent_request_count = len(self.ticket_log_talametry[source_ip])
        print(f"[AUDIT] Active requests in last {self.time_window_sec}s window for {source_ip}: {recent_request_count}")
        
        if recent_request_count > self.max_requests:
            self.trigger_incident_response(source_ip, account_name)
    
    def trigger_incident_response(self, offending_ip, account):
        print(f"\n🚨🚨 [CRITICAL ALERT] INFRASTRUCTURE SECURITY BREACH SUSPECTED! 🚨🚨")
        print(f"    [REASON] Host {offending_ip} exceeded TGS request threshold ({self.max_requests} reqs/{self.time_window_sec}s).")
        print(f"    [TARGET USER] Token context associated with: {account}")
        print(f"    [ACTION] Dynamic Active Directory Mitigation Engaged.")
        print(f"    [💥 RISK SHIELD] Host {offending_ip} has been ISOLATED via corporate firewall rules.")
        self.isolated_ips.add(offending_ip)

if __name__ == "__main__":
    auditor = EnterpriseKerberosAuditor(time_window_sec=5, max_requests=2)
    
    # Normal Traffic Simulation
    auditor.process_event_4769("10.10.10.50", "hr_user", "http/intranet.corp.local", "AES256-CTS-HMAC-SHA1-96")
    time.sleep(6) # Waiting for the time window to reset
    
    # Rapid and Suspicious Attack Traffic Simulation (Kerberoasting Begins)
    auditor.process_event_4769("10.10.10.99", "pentest_agent", "MSSQLSvc/sql-prod.corp.local:1433", "RC4-HMAC")
    auditor.process_event_4769("10.10.10.99", "pentest_agent", "http/web-internal.corp.local", "AES256-CTS-HMAC-SHA1-96")
    
    # 3rd rapid request exceeding the threshold (Alarm triggered)
    auditor.process_event_4769("10.10.10.99", "pentest_agent", "HOST/backup-dc.corp.local", "AES256-CTS-HMAC-SHA1-96")
    
    # Request after being blocked
    auditor.process_event_4769("10.10.10.99", "pentest_agent", "some/other-spn", "RC4-HMAC")