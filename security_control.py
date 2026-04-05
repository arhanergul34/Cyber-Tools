# We are setting a target password
target_password = "cyber123"

# We are collecting input from the user
entered_password = input("Enter the password to log in to the system: ")

# Desicion making phase
if entered_password == target_password:
    print ("----------------------------------")
    print ("[+] Access Approved! Welcome to the system. ")
    print ("----------------------------------")
else:
    print ("----------------------------------")
    print ("[-] INCORRECT PASSWORD! Access Denied. ")
    print ("----------------------------------")
    
    