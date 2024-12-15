import bcrypt
from cryptography.fernet import Fernet

def write_key():
    key = Fernet.generate_key()
    with open("key.key", 'wb') as key_file:
        key_file.write(key)

def load_key():
    try:
        with open("key.key", "rb") as file:
            key = file.read()
        return key
    
    except FileNotFoundError:
        print("Key file not found. Generating a new key.")
        write_key()
        return load_key()

def create_master_password():
    try:
        with open("master_password.txt", "rb") as f:
            print("Master password is already set.")
            
    except FileNotFoundError:
        master_pass = input("Set your master password: ")
        hashed = bcrypt.hashpw(master_pass.encode(), bcrypt.gensalt())
        with open("master_password.txt", "wb") as f:
            f.write(hashed)
        print("Master password set successfully!")

def verify_master_password():
    try:
        with open("master_password.txt", "rb") as f:
            stored_hashed_pass = f.read()
            
        master_pass = input("Enter your master password: ")
        if bcrypt.checkpw(master_pass.encode(), stored_hashed_pass):
            print("Access granted.")
            return True
        
        else:
            print("Access denied. Incorrect master password.")
            return False
        
    except FileNotFoundError:
        print("No master password set. Please set it first.")
        create_master_password()
        return verify_master_password()

key = load_key()
fer = Fernet(key)

def view():
    try:
        with open('password.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                
                if data.count("|") == 2:
                    platform, user, enc_password = data.split("|")
                    print(f"Platform: {platform} \nUser: {user} \nPassword: {fer.decrypt(enc_password.encode()).decode()} \n")
                
                else:
                    print(f"Malformed line in file: {data}")
                    
    except FileNotFoundError:
        print("No passwords stored yet.")

def add():
    platform = input("Platform: ")
    user = input("Username: ")
    password = input("Password: ")
    
    with open('password.txt', 'a') as f:
        f.write(platform + "|" + user + "|" + fer.encrypt(password.encode()).decode() + "\n")
    print("Password added successfully!")

create_master_password()

if not verify_master_password():
    exit()

while True:
    inp = input("You can view or add your password (Enter: view, add) or type q to quit: ").lower()
    
    if inp == "q":
        break
    
    elif inp == "view":
        view()
        
    elif inp == "add":
        add()
        
    else:
        print("Invalid Input, Please try again.")
