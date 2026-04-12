# brute_force_sim.py
# This tool reads a wordlist file and simulates a password guessing exercise.

def wordlist_read():
    print("[...] Reading the file, please wait...")
    try:
        with open("wordlist.txt", "r", encoding="utf-8") as file:
            passwords = file.readlines()
            print(f"[+] {len(passwords)} passwords have been loaded.")

            true_password = "root"
            
            for password in passwords:
                clear_password = password.strip()
                print(f"[!] Being tried: {clear_password}")
                
                if clear_password == true_password:
                    print(f"[+] BINGO! Password Found: {clear_password}")
                    break 
                    
    except FileNotFoundError:
        print("[-] ERROR: File 'wordlist.txt' not found! Please create the file.") 
        
wordlist_read()         






