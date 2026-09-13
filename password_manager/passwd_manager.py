import os
import json
import hashlib as hl
from getpass import getpass as gp

def generate_hash(password):
    """Generate a SHA-256 hash of the given password."""
    return hl.sha256(password.encode()).hexdigest()

def create_master_passwd():
    if not os.path.exists("password_manager/config.json") or os.path.getsize("password_manager/config.json") == 0 or (os.path.exists("password_manager/config.json") and json.load(open("password_manager/config.json")) == {}):
        with open("password_manager/config.json", "w") as f:
            passwd = gp("Enter a password to secure your password manager: ")
            hashed_passwd = generate_hash(passwd)
            json.dump({"password": hashed_passwd}, f)
            print("Master password created and password saved!")

def check_master_passwd():
    with open("password_manager/config.json", "r") as file:
        master_passwd = gp("Enter the master password: ")
        entered_hashed_master_passwd = generate_hash(master_passwd)
        current_hashed_master_password = json.load(file)["password"]
        

    return entered_hashed_master_passwd, current_hashed_master_password

def encrypt_passwd(passwd):
    bin_passwd = " ".join(f"{ord(char):08b}" for char in passwd) #converts each character in the password into binary bytes
    xor_bin_passwd = ""

    #flips the "polarity" of the bits (xor encryption)
    for byte in bin_passwd:
        for bit in byte:
            if bit == "0":
                xor_bin_passwd += "1"
            elif bit == "1":
                xor_bin_passwd += "0"

    hex_passwd = hex(int(xor_bin_passwd, 2))[2:] #final step by converting the giant binary value into hexadecimal, the [2:] to strip off the beginning "0x"
    return hex_passwd

def decrypt_passwd(passwd): 
    bin_len = len(passwd) * 4
    bin_passwd = bin(int(passwd, 16))[2:].zfill(bin_len)
    xor_bin_passwd = ""

    for bit in bin_passwd:
        if bit == "0":
            xor_bin_passwd += "1"
        elif bit == "1":
            xor_bin_passwd += "0"

    plain_text = ""
    for i in range(0, len(xor_bin_passwd), 8):
        byte_chunk = xor_bin_passwd[i:i+8]
        plain_text += chr(int(byte_chunk, 2))

    return plain_text

create_master_passwd()

option = input('Enter "1" to add a new password, "2" to view vault or "3" to view the unencrypted passwords: ')

if option == "1":
    entered_hashed_master_passwd, current_hashed_master_password = check_master_passwd()

    #compares is both hashes are the same
    if entered_hashed_master_passwd == current_hashed_master_password:
        website = input("Enter the website name: ")
        username = input("Enter your username: ")
        passwd = gp("Enter your password: ")

        try:
            encrypted_passwd = encrypt_passwd(passwd)
        except ValueError:
            print("Invalid password, please enter a valid password.")
            exit()

        # fetches the vault's data
        if os.path.exists("password_manager/vault.json") and os.path.getsize("password_manager/vault.json") > 0:
            with open("password_manager/vault.json", "r") as file:
                data = json.load(file)
        else:
            data = {}

        data[website] = {"username": username, "password": encrypted_passwd}

        #saves the new data
        with open("password_manager/vault.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Password saved successfully!")

    else:
        print("Incorrect password, try again!")

elif option == "2":
    entered_hashed_master_passwd, current_hashed_master_password = check_master_passwd()
    if entered_hashed_master_passwd == current_hashed_master_password:
        if os.path.exists("password_manager/vault.json") and os.path.getsize("password_manager/vault.json") > 0:
            with open("password_manager/vault.json", "r") as file:
                try:
                    vault_data = json.load(file)
                    if vault_data == {}:
                        print("Your vault is currently empty.")
                    else:
                        print(vault_data)
                except json.JSONDecodeError:
                    print("Your vault is currently empty or corrupted.")
        else:
            print("Your vault is currently empty.")

    else:
        print("Incorrect password, try again!")

elif option == "3":
    entered_hashed_master_passwd, current_hashed_master_password = check_master_passwd()

    if entered_hashed_master_passwd == current_hashed_master_password:
        if os.path.exists("password_manager/vault.json") or os.path.getsize("password_manager/vault.json") == 0 or (os.path.exists("password_manager/vault.json") and json.load(open("password_manager/vault.json")) == {}):
            with open("password_manager/vault.json", "r") as file:
                data = json.load(file)
                website_choice = input("Which website's password do you want to view: ").strip()
                website_passwd = data[website_choice]["password"]
                decrypted_passwd = decrypt_passwd(website_passwd)
            
                if website_choice in data:
                    print(f"Here's your decrypted password to {website_choice}: {decrypted_passwd}")
        else:
            print("No passwords have been added")
    else:
        print("Incorrect password, try again!")

else:
    print("Invalid option")
