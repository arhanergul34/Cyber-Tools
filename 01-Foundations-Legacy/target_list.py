# List of IP addresses to scan
targets = ["192.168.1.1", "192.168.1.15", "10.0.0.5", "172.16.0.100"]

print(f"A total of {len(targets)} targets have been set.")

#Let's add a new target to the list (as if a new device had been discovered).
new_target = "192.168.1.50"
targets.append(new_target)

print("--- SCREENING BEGINS ---")

#Let's print each target to the screen in turn (using While).
for target in targets:
    print(f"[WAIT] {target} scanning address...")
    
print("--- SCAN COMPLETED ---")