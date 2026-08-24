import time
import random
import json
from typing import Dict

class RedTeamJitterBeacon:
    """
    Offensive C2 Beaconing Engine with Adaptive Jitter Implementation.
    Designed to evade network timing-analysis and SOC beacon detection rules.
    """
    def __init__(self, base_interval: float = 10.0, jitter_percentage: float = 0.30):
        """
        :param base_interval: Target wait time between check-ins (in seconds)
        :param jitter_percentage: Fluctation ratio (e.g., 0.30 = +/- 30% variation)
        """
        self.base_interval = base_interval
        self.jitter_percentage = jitter_percentage
        self.agent_id = "AGENT_NODE_8821"
    
    def calculate_next_sleep_interval(self) -> float:
        """
        Calculates a randomized sleep duration using the jitter formula:
        Interval = Base_Interval +/- (Base_Interval * Jitter_Percentage * Random_Factor)
        """
        max_delta = self.base_interval * self.jitter_percentage
        # Generates a random float between -max_delta and +max_delta
        random_delta = random.uniform(-max_delta, max_delta)
        
        # Ensures the calculated interval never drops below a safe minimum threshold (e.g., 0.5s)
        actual_sleep = max(0.5, self.base_interval + random_delta)
        return round(actual_sleep, 4)
    
    def generate_beacon_packet(self, seq_number: int, sleep_duration: float) -> str:
        """
        Constructs a simulated outgoing HTTP/JSON C2 Check-in packet payload.
        """
        payload = {
            "agent_id": self.agent_id,
            "seq": seq_number,
            "status": "CHECK_IN",
            "next_interval_sec": sleep_duration
        }
        return json.dumps(payload)

if __name__ == "__main__":
    print("==================================================")
    print(" OFFENSIVE C2 BEACONING & JITTER GENERATOR ENGINE")
    print("==================================================\n")

    # Base interval = 10s, Jitter = %30 (+/- 3 seconds window)
    c2_agent = RedTeamJitterBeacon(base_interval=10.0, jitter_percentage=0.30)
    
    print(f"[*] Configuration Base Interval = {c2_agent.base_interval}s | Jitter = {int(c2_agent.jitter_percentage * 100)}%")
    print("[*] Simulating 5 consecutive C2 check-in cycles...\n")
    
    for cycle in range(1, 6):
        # 1. Calculate randomized delay
        next_sleep = c2_agent.calculate_next_sleep_interval()
        
        # 2. Construct simulated check-in payload
        beacon_pkg = c2_agent.generate_beacon_packet(seq_number=cycle, sleep_duration=next_sleep)
        
        print(f"[Cycle #{cycle} Beacon Sent: {beacon_pkg}]")
        print(f"        -> Next check-in in: {next_sleep} seconds (Jitter applied)")
        
        # In a real scenario, time.sleep(next_sleep) would be executed here.