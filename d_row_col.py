# ---------------------------------------------------------------
# Row-Column & Double Row-Column Transposition Cipher
# Menu-driven implementation with encryption & decryption
# ---------------------------------------------------------------

def chunk_text(text, size):
    """Divide text into equal chunks (rows)."""
    return [text[i:i+size] for i in range(0, len(text), size)]


def pad_text(text, size):
    """Pad plaintext so matrix is complete."""
    if len(text) % size != 0:
        padding = size - (len(text) % size)
        text += "X" * padding
    return text


# ---------------------------------------------------------------
# SINGLE ROW-COLUMN ENCRYPTION
# ---------------------------------------------------------------
def encrypt_row_column(plaintext, rows):
    plaintext = plaintext.replace(" ", "").upper()
    cols = (len(plaintext) + rows - 1) // rows
    plaintext = pad_text(plaintext, rows)

    matrix = chunk_text(plaintext, cols)

    print("\n[Matrix Used For Encryption:]")
    for row in matrix:
        print(" ".join(row))

    ciphertext = ""
    for c in range(cols):
        for r in range(rows):
            if c < len(matrix[r]):
                ciphertext += matrix[r][c]

    return ciphertext


# ---------------------------------------------------------------
# SINGLE ROW-COLUMN DECRYPTION
# ---------------------------------------------------------------
def decrypt_row_column(ciphertext, rows):
    ciphertext = ciphertext.replace(" ", "").upper()
    cols = (len(ciphertext) + rows - 1) // rows

    matrix = [[""] * cols for _ in range(rows)]

    index = 0
    for c in range(cols):
        for r in range(rows):
            if index < len(ciphertext):
                matrix[r][c] = ciphertext[index]
                index += 1

    print("\n[Matrix Used For Decryption:]")
    for row in matrix:
        print(" ".join(row))

    plaintext = "".join("".join(row) for row in matrix)
    return plaintext


# ---------------------------------------------------------------
# DOUBLE TRANSPOSITION
# ---------------------------------------------------------------
def double_encrypt(text, r1, r2):
    print("\n--- ROUND 1 ---")
    c1 = encrypt_row_column(text, r1)
    print("Cipher after round 1:", c1)

    print("\n--- ROUND 2 ---")
    c2 = encrypt_row_column(c1, r2)
    print("Final Cipher:", c2)
    return c2


def double_decrypt(cipher, r1, r2):
    print("\n--- REVERSE ROUND 1 ---")
    p1 = decrypt_row_column(cipher, r2)
    print("Intermediate:", p1)

    print("\n--- REVERSE ROUND 2 ---")
    p2 = decrypt_row_column(p1, r1)
    print("Final Plaintext:", p2)
    return p2


# ---------------------------------------------------------------
# MENU
# ---------------------------------------------------------------
while True:
    print("\n---------------- MENU ----------------")
    print("1. Encrypt (Single Row-Column)")
    print("2. Decrypt (Single Row-Column)")
    print("3. Double Encryption")
    print("4. Double Decryption")
    print("5. Exit")
    print("-------------------------------------")

    choice = input("Choose option: ")

    if choice == "1":
        text = input("Enter plaintext: ")
        rows = int(input("Enter number of rows: "))
        print("Ciphertext:", encrypt_row_column(text, rows))

    elif choice == "2":
        text = input("Enter ciphertext: ")
        rows = int(input("Enter number of rows: "))
        print("Plaintext:", decrypt_row_column(text, rows))

    elif choice == "3":
        text = input("Enter plaintext: ")
        r1 = int(input("Enter rows for round 1: "))
        r2 = int(input("Enter rows for round 2: "))
        print("Double Encrypted Cipher:", double_encrypt(text, r1, r2))

    elif choice == "4":
        text = input("Enter ciphertext: ")
        r1 = int(input("Enter rows for round 1 (used during encryption): "))
        r2 = int(input("Enter rows for round 2 (used during encryption): "))
        print("Double Decrypted Plaintext:", double_decrypt(text, r1, r2))

    elif choice == "5":
        print("Exiting...")
        break

    else:
        print("Invalid choice! Try again.")
