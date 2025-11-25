# --------------------------------------------
# MONOALPHABETIC SUBSTITUTION CIPHER
# Encryption, Decryption, Exit (Menu Driven)
# --------------------------------------------

# Fixed substitution key (You can modify)
# Plain : ABCDEFGHIJKLMNOPQRSTUVWXYZ
# Cipher: QWERTYUIOPASDFGHJKLZXCVBNM

key = {
    'A':'Q','B':'W','C':'E','D':'R','E':'T','F':'Y','G':'U','H':'I','I':'O','J':'P',
    'K':'A','L':'S','M':'D','N':'F','O':'G','P':'H','Q':'J','R':'K','S':'L','T':'Z',
    'U':'X','V':'C','W':'V','X':'B','Y':'N','Z':'M'
}

# Reverse key for decryption
rev_key = {v: k for k, v in key.items()}


# ---------------- Encryption Function ----------------
def encrypt(plaintext):
    plaintext = plaintext.upper()
    cipher = ""

    for ch in plaintext:
        if ch.isalpha():
            cipher += key[ch]
        else:
            cipher += ch     # keep spaces/punctuation same

    return cipher


# ---------------- Decryption Function ----------------
def decrypt(ciphertext):
    ciphertext = ciphertext.upper()
    plain = ""

    for ch in ciphertext:
        if ch.isalpha():
            plain += rev_key[ch]
        else:
            plain += ch

    return plain


# -------------------- MENU --------------------------
while True:
    print("\n-------- Monoalphabetic Cipher --------")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")
    print("----------------------------------------")

    choice = input("Enter your choice: ")

    if choice == '1':
        text = input("Enter plaintext: ")
        encrypted = encrypt(text)
        print("Encrypted Text:", encrypted)

    elif choice == '2':
        text = input("Enter ciphertext: ")
        decrypted = decrypt(text)
        print("Decrypted Text:", decrypted)

    elif choice == '3':
        print("Exiting program...")
        break

    else:
        print("Invalid choice! Try again.")
