import json
import re
from typing import Dict, List, Tuple

class BlueTeamHTTPInspector:
    """
    Defensive HTTP Traffic Inspection Engine.
    Analyzes HTTP headers, User-Agent consistency, and payload anomalies to detect Malleable C2 profiles.
    """
    def __init__(self, anomaly_threshold: int = 30):
        self.anomaly_threshold = anomaly_threshold
        # Tracks active sessions and their observed User-Agents for consistency checking
        self.session_user_agents: Dict[str, str] = {}
    
    def _is_base64_encoded(self, text: str) -> bool:
        """Helper method: Detects if a given string string displays Base64 encoding characteristics."""
        if len(text) % 4 != 0:
            return False
        base64_pattern = r'^[A-Za-z0-9+/]+={0,2}$'
        return bool(re.match(base64_pattern, text))
    
    def inspect_http_request(self, uri: str, headers: Dict[str, str], body: str = "") -> Dict:
        """
        Inspects an incoming HTTP Request and calculates an overall Anomaly Score.
        Returns a threat evaluation report.
        """
        anomaly_score = 0
        detected_indicators: List[str] = []
        
        user_agent = headers.get("User-Agent", "")
        host = headers.get("Host", "")
        cookie = headers.get("Cookie", "")
        
        # Indicator 1: Missing Essential HTTP Headers
        if not user_agent or not host:
            anomaly_score += 25
            detected_indicators.append("SUSPICICOUS_TELEMETRY_URI_PATTERN")
        
        # Indicator 3: User-Agent Spoofing / Inconsistency Tracking
        # Extract fake session ID or use Host as identifier
        session_key = host
        if session_key in self.session_user_agents:
            previous_ua = self.session_user_agents[session_key]
            if previous_ua != user_agent:
                anomaly_score += 25
                detected_indicators.append(f"USER_AGENT_MISMATCH_IN_SESSION (Prev: {previous_ua[:20]}... vs Curr: {user_agent[:20]}...)")
        else:
            self.session_user_agents[session_key] = user_agent
            
        # Indicator 4: Obfuscated Base64 Data in Cookie
        if cookie and "__ga_session=" in cookie:
            # Extract cookie payload
            cookie_payload = cookie.split("__ga_session=")[1].split(";")[0]
            if self._is_base64_encoded(cookie_payload):
                anomaly_score += 20
                detected_indicators.append("BASE64_OBFUSCATED_COOKIE_PAYLOAD")
        
        # Indicator 5: Encapsulated Base64 Data in POST Body
        if body:
            try:
                json_body = json.loads(body)
                metric_data = json_body.get("metric_data", "")
                if metric_data and self._is_base64_encoded(metric_data):
                    anomaly_score += 25
                    detected_indicators.append("BASE64_EXFILTRATION_PAYLOAD_IN_BODY")
            except json.JSONDecodeError:
                pass
        
        is_threat = anomaly_score >= self.anomaly_threshold
        
        return {
            "threat_detected": is_threat,
            "anomaly_score": anomaly_score,
            "threshold": self.anomaly_threshold,
            "indicators": detected_indicators,
            "verdict": "MALLEABLE_C2_TRAFFIC" if is_threat else "CLEAN_TRAFFIC"
        }            
        
if __name__ == "__main__":
    from offensive_c2_http_profile import RedTeamMalleableHTTPProfile
    
    print("==================================================")
    print(" BLUE TEAM NIDS: HTTP TRAFFIC INSPECTOR")
    print("==================================================\n")
    
    http_inspector = BlueTeamHTTPInspector(anomaly_threshold=30)
    attacker = RedTeamMalleableHTTPProfile()
    
  # 1. Inspecting Attacker's GET Check-in Request
    get_uri, get_headers = attacker.create_get_checkin_request()
    get_report = http_inspector.inspect_http_request(get_uri, get_headers)

    print("[1] Inspection Result for Incoming GET Request:")
    print(f" -> Threat Detected: {get_report['threat_detected']}")
    print(f" -> Anomaly Score: {get_report['anomaly_score']}")
    print(f" -> Indicators: {get_report['indicators']}")
    print(f" -> Verdict: {get_report['verdict']}\n")

    # 2. Inspecting Attacker's POST Exfiltration Request
    sample_output = "Desktop-PC\\Admin_User - Privilege Level: HIGH"
    post_uri, post_headers, post_body = attacker.create_post_exfiltration_request(sample_output)
    post_report = http_inspector.inspect_http_request(post_uri, post_headers, post_body)

    print("[2] Inspection Result for Incoming POST Request:")
    print(f" -> Threat Detected: {post_report['threat_detected']}")
    print(f" -> Anomaly Score: {post_report['anomaly_score']}")
    print(f" -> Indicators: {post_report['indicators']}")
    print(f" -> Verdict: {post_report['verdict']}\n")