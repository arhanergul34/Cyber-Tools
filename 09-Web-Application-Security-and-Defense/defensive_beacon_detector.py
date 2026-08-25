import math
from typing import List, Dict
from offensive_c2_jitter import RedTeamJitterBeacon

class BlueTeamBeaconDetector:
    """
    Defensive Timing Analysis Engine.
    Detects C2 Beacons by calculating the Standard Deviation of packet arrival intervals.
    """
    def __init__(self, max_std_dev_threshold: float = 4.0):
        # If the standard deviation of the time differences is below this value, the system is considered robotic.
        self.max_std_dev_threshold = max_std_dev_threshold
        self.arrival_times: List[float] = []
    
    def record_packet_arrival(self, timestamp: float):
        """It records the arrival time (timestamp) of the packet captured from the network into the list."""
        self.arrival_times.append(timestamp)
    
    def analyze_timing_anomalies(self) -> Dict:
        """It statistically analyzes the differences between recorded arrival times."""
        packet_count = len(self.arrival_times)
        
        # Statistical analysis cannot be performed without at least 3 packages.
        deltas = []
        for i in range(1, packet_count):
            time_difference = self.arrival_times[i] - self.arrival_times[i - 1]
            deltas.append(time_difference)
        
        # 2. Calculate Average Waiting Time (Mean)
        mean_delta = sum(deltas) / len(deltas)
        
        # 3. Calculate the Standard Deviation
        # (The square of the distance of each difference from the mean)
        variance_sum = 0
        for delta in deltas:
            variance_sum += (delta - mean_delta) ** 2
        
        variance = variance_sum / len(deltas)
        std_dev = math.sqrt(variance)
        
        # 4. Detection Logic: If the standard deviation is low, the behavior is too regular to be human.
        is_suspicious = std_dev < self.max_std_dev_threshold
        
        return {
            "threat_detected": is_suspicious,
            "analyzed_packets": packet_count,
            "mean_interval_sec": round(mean_delta, 2),
            "std_deviation": round(std_dev, 4),
            "signature": "BEACONING_ANOMALY" if is_suspicious else "NORMAL_TRAFFIC"
        }

if __name__ == "__main__":
    print("==================================================")
    print(" BLUE TEAM NIDS: BEACON TIMING ANALYSIS")
    print("==================================================\n")
    
    # 1. Launching the Red Team agent (10-second target, 30% deviation)
    attacker = RedTeamJitterBeacon(base_interval=10.0, jitter_percentage=0.30)
    detector = BlueTeamBeaconDetector()
    
    # 2. Simulation: Network traffic timeline (We assume the first packet arrived at the 0th second)
    current_time = 0.0
    print("[*] Network traffic is being monitored, and packet arrival times are being recorded...\n")
    
    # We are simulating the arrival of a 20-unit package.
    for i in range(20):
        detector.record_packet_arrival(current_time)
        
        # We calculate when the attacker will send the next packet.
        next_sleep = attacker.calculate_next_sleep_interval()
        
        # Time is passing... (In real life, this would be `time.sleep`; here, we're fast-forwarding time.)
        current_time += next_sleep
        
    # 3. Blue Team Analysis
    analysis_result = detector.analyze_timing_anomalies()
    
    print("[!] Statistical Analysis Result:")
    for key, value in analysis_result.items():
        print(f" -> {key}: {value}")
        
                