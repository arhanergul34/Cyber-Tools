from concurrent.futures import ThreadPoolExecutor
import time
import random

# STEP 1: Agent's Mission Description
def cyber_task(target_id):
    """
    This function simulates a cybersecurity task. For example: scanning a port or trying a password.
    """
    print(f"[>] Processing task {target_id}...")
    
    # Let's simulate network latency (between 1 and 4 seconds)
    duration = random.uniform(1, 4)
    time.sleep(duration)
    
    print(f"[+] Task {target_id} COMPLETED. (Time: {duration:.2f}s)")
    return f"Result {target_id}"


# STEP 2: Objective List
# Let's say we have 10 tasks
targets = range(1, 11)

print("---CONTROLLED CYBER OPERATION BEGINS (Max. 3 Simultaneous) ---\n")
start_time = time.time()

# STEP 3: ARCHITECTURE CENTER - ThreadPoolExecutor
# By saying 'max_workers=3', we allow only 3 threads to run at the same time.
with ThreadPoolExecutor(max_workers=3) as executor:
    # The 'map' function sends each item in the 'targets' list to 'cyber_task'.
    # But it uses 3 workers in the pool to do this.
    results = executor.map(cyber_task, targets)
    
# STEP 4: Reporting
end_time = time.time()
print(f"\n[!] The operation ended successfully. ")
print(f"[!] Total elapsed time: {end_time - start_time:.2f} second.")
      