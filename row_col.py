# Row-Column Rail Fence Transposition Cipher (Menu Driven)

def encrypt(message, key):
    message = message.replace(" ", "").upper()
    print("\n[Encryption] Cleaned Message:", message)

    # Calculate required columns
    cols = -(-len(message) // key)  # ceiling division

    print(f"[Encryption] Rows = {key}, Columns = {cols}")

    # Fill row-wise
    matrix = []
    idx = 0
    for r in range(key):
        row = []
        for c in range(cols):
            if idx < len(message):
                row.append(message[idx])
                idx += 1
            else:
                row.append('X')  # padding
        matrix.append(row)

    print("\n[Encryption] Matrix (Row-wise filled):")
    for row in matrix:
        print(" ".join(row))

    # Read column-wise
    cipher = ""
    for c in range(cols):
        for r in range(key):
            cipher += matrix[r][c]

    return cipher


def decrypt(cipher, key):
    cipher = cipher.replace(" ", "").upper()
    print("\n[Decryption] Cipher Text:", cipher)

    cols = -(-len(cipher) // key)
    print(f"[Decryption] Rows = {key}, Columns = {cols}")

    # Fill column-wise
    matrix = [["" for _ in range(cols)] for _ in range(key)]

    idx = 0
    for c in range(cols):
        for r in range(key):
            if idx < len(cipher):
                matrix[r][c] = cipher[idx]
                idx += 1

    print("\n[Decryption] Matrix (Column-wise filled):")
    for row in matrix:
        print(" ".join(row))

    # Read row-wise
    plaintext = ""
    for r in range(key):
        for c in range(cols):
            plaintext += matrix[r][c]

    return plaintext


def main():
    while True:
        print("\n===== ROW-COLUMN RAIL FENCE CIPHER =====")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        
        ch = input("Enter choice: ")

        if ch == "1":
            msg = input("Enter message: ")
            key = int(input("Enter key (number of rows): "))
            cipher = encrypt(msg, key)
            print("\n[Result] Cipher Text:", cipher)

        elif ch == "2":
            cipher = input("Enter cipher text: ")
            key = int(input("Enter key (number of rows): "))
            plain = decrypt(cipher, key)
            print("\n[Result] Decrypted Message:", plain)

        elif ch == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

# Run the menu
main()
