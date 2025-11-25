def generate_key(text, key):
    key = list(key)
    if len(text) == len(key):
        return "".join(key)
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def encrypt(text, key):
    cipher = []
    for i in range(len(text)):
        if text[i].isalpha():
            shift = ord(key[i].upper()) - ord('A')
            base = ord('A') if text[i].isupper() else ord('a')
            cipher_char = chr((ord(text[i]) - base + shift) % 26 + base)
            cipher.append(cipher_char)
        else:
            cipher.append(text[i])  # keep spaces/punctuation
    return "".join(cipher)

def decrypt(cipher, key):
    text = []
    for i in range(len(cipher)):
        if cipher[i].isalpha():
            shift = ord(key[i].upper()) - ord('A')
            base = ord('A') if cipher[i].isupper() else ord('a')
            plain_char = chr((ord(cipher[i]) - base - shift + 26) % 26 + base)
            text.append(plain_char)
        else:
            text.append(cipher[i])
    return "".join(text)

# -------------------- MENU --------------------
while True:
    print("\n--- Polyalphabetic (Vigenere) Cipher ---")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        text = input("Enter plaintext: ")
        key = input("Enter key: ")
        full_key = generate_key(text, key)
        print("Generated Key:", full_key)
        cipher = encrypt(text, full_key)
        print("Encrypted Text:", cipher)

    elif choice == "2":
        cipher = input("Enter ciphertext: ")
        key = input("Enter key: ")
        full_key = generate_key(cipher, key)
        print("Generated Key:", full_key)
        text = decrypt(cipher, full_key)
        print("Decrypted Text:", text)

    elif choice == "3":
        print("Exiting program...")
        break

    else:
        print("Invalid option! Try again.")
