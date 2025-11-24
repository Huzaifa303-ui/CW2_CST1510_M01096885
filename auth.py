import bcrypt
import os

def hash_password(plain_text_password):
   
    # TODO: Encode the password to bytes (bcrypt requires byte strings)
    password_bytes = plain_text_password.encode('utf-8')
    
    # TODO: Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()
    
    # TODO: Hash the password using bcrypt.hashpw()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    # TODO: Decode the hash back to a string to store in a text file
    hashed_password_str = hashed_password.decode('utf-8')
    
    
    return hashed_password_str


def verify_password(plain_text_password, stored_hash):
    # Encode both the plaintext password and the stored hash to bytes
    password_bytes = plain_text_password.encode('utf-8')
    stored_hash_bytes = stored_hash.encode('utf-8')
    
    # Use bcrypt.checkpw() to verify the password
    # This function extracts the salt from the stored hash and compares
    is_valid = bcrypt.checkpw(password_bytes, stored_hash_bytes)
    
    return is_valid


# TEMPORARY TEST CODE - Remove after testing
test_password = "SecurePassword123"
    
# Test hashing
hashed = hash_password(test_password)
print(f"Original password: {test_password}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")
 # Test verification with correct password
is_valid = verify_password(test_password, hashed)
(f"\nVerification with correct password: {is_valid}")
 # Test verification with incorrect password
is_invalid = verify_password("WrongPassword", hashed)
print(f"Verification with incorrect password: {is_invalid}")


USER_DATA_FILE = "users.txt"

def register_user(username, password, filename="users.txt"):
    # Check if the username already exists
    try:
        with open(filename, "r") as file:
            for line in file:
                stored_username, _ = line.strip().split(",", 1)
                if stored_username == username:
                    print("Username already exists.")
                    return False
    except FileNotFoundError:
        # If the file doesn't exist, it will be created later
        pass

    # Hash the password
    password_hash = hash_password(password)

    # Append the new user to the file in the format: username,hashed_password
    with open(filename, "a") as file:
        file.write(f"{username},{password_hash}\n")

    print("User registered successfully.")
    return True

def user_exists(username, filename="users.txt"):
    try:
        # Handle the case where the file doesn't exist yet
        with open(filename, "r") as file:
            # Read the file and check each line for the username
            for line in file:
                stored_username, _ = line.strip().split(",", 1)
                if stored_username == username:
                    return True
    except FileNotFoundError:
        # If the file doesn't exist, no users are registered yet
        return False

    return False

def login_user(username, password, filename="users.txt"):
    try:
        # Handle the case where no users are registered yet
        with open(filename, "r") as file:
            # Search for the username in the file
            for line in file:
                stored_username, stored_hash = line.strip().split(",", 1)
                
                if stored_username == username:
                    # If username matches, verify the password
                    if verify_password(password, stored_hash):
                        print("Login successful!")
                        return True
                    else:
                        print("Incorrect password.")
                        return False
    except FileNotFoundError:
        # If the file doesn't exist, no users are registered yet
        print("No users registered yet.")
        return False

    # If we reach here, the username was not found
    print("Username not found.")
    return False

def validate_username(username):
    import re
    # Check if username is empty
    if not username:
        return False, "Username cannot be empty."
    
    # Check length (for example: 3–20 characters)
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters long."
    
    # Check allowed characters (letters, numbers, underscores only)
    if not re.match(r"^[A-Za-z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores."
    
    # If all checks pass
    return True, "Valid username."

def validate_password(password):
    import re
    # Check if password is empty
    if not password:
        return False, "Password cannot be empty."
    
    # Check length (at least 8 characters)
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    
    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    
    # Check for at least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    
    # Check for at least one number
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    
    # If all checks pass
    return True, "Valid password."

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("  Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)


def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password = input("Enter a password: ").strip()

            
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            # Register the user
            register_user(username, password)
        
        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard or protected resources.)")
                
                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")
        
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")
        
if __name__ == "__main__":
    main()
