def secure_login():
    try:
        # This is the part where mistakes are possible.
        port = int(input("Please enter the port number you wish to scan: "))
        print(f"[+] Preparing a scan for port {port}...")
    
    except ValueError:
        # This will run if there is a 'Value Error' above.
        print("[-] ERROR: Please enter only NUMBERS! Letters are not accepted.")
    
    except Exception as error:
        # This will come into play if another unexpected error occurs.
        print(f"[!] An unexpected error occurred: {error}")
    
    finally:
        # Part that will always work, whether there's a bug or not
        print("[*] The transaction attempt was completed.")
        
# Lets call the function
secure_login()    
          
