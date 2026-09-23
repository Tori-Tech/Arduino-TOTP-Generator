import time 

def check_login():
    print("=== Login Portal ===")
    
    while True:
        username = input("\nUsername: ")
        password = input("Enter your 6-digit TOTP code (or 'q' to quit): ")

        if password.lower() == 'q':
            print("Exiting portal.")
            break

        try:
            with open("active_totp.txt", "r") as f:
                correct_code = f.read().strip()
            
            if username == "admin" and password == correct_code:
                print("Access granted. Welcome, admin.")
                break # exit the loop upon successful login
            else:
                print("Access denied: Invalid credentials.")
                
        except FileNotFoundError:
            print("Error: The TOTP server isn't running or hasn't generated a code yet.")
            break

if __name__ == "__main__":
    check_login()
