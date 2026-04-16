import threading
import time
import random

# Cybersecurity Scenario: An attempted system login
def login_attempt(username):
    print(f"[!] Login attempt started for {username}...")
    # We are waiting for the system's response (Network latency simulation)

    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)
    
    # Let's generate a random result
    if random.choice([True, False]):
        print(f"[+] SUCCESSFUL: {username} logged into the system! (Time: {sleep_time:.2f}s)")
    else:
        print(f"[-] UNSUCCESSFUL: {username} incorrect password. (Time: {sleep_time:.2f}s)")
        
# List of users to attack
users_to_attack = ["admin", "root", "guest", "test_user", "db_admin"]

print("---Cybersecurity Multiple Access Simulation Begins ---\n")
start_time = time.time()

# Thread List
active_threads = []

for user in users_to_attack:
    # We create a separate thread (agent) for each user.
    t = threading.Thread(target=login_attempt, args=(user,))
    active_threads.append(t)
    t.start() # Release the agent

# Wait for all trials to finish
for t in active_threads:
    t.join()
    
end_time = time.time()
print(f"\n[!] Total Operation Time: {end_time - start_time:.2f} second.")
