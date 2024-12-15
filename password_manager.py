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

key = load_key()
fer = Fernet(key)

def view():
    try:
        with open('password.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                
                if data.count("|") == 2:  # Check for correct format
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

master_pass = input("Enter your master password: ")

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
