# Target Informations
target_user = "admin"
target_password = "cyber123"

# We are collecting input from the user
entered_name = input("Enter your username: ")
entered_password = input("Enter your password : ")

# We check both conditions simultaneously.
if target_user == entered_name  and entered_password == target_password:
    print ("----------------------------------")
    print ("[+] Login Successful! Welcome, Administrator. ")
    print ("----------------------------------")
else:
    print ("----------------------------------")
    print ("[-] ERROR: Incorrect username or password! ")
    print ("----------------------------------")
    
    