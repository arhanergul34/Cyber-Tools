target_password = "cyber123"
chance = 3  # User's total trial rights

while chance > 0:
    entered = input(f"You have {chance} chance left to log in to the system. Password: ")
    
    if entered == target_password:
        print("[+] Login Successful! The system has been hacked. ")
        break # If the password is correct, exit the loop immediately!
    else:
        chance = chance - 1 # Each mistake reduces one chance
        print("[-] Incorrect Password. ")
        
if chance == 0:
    print("[!!!] ACCOUNT BLOCKED! Too many failed attempts. ")
    