import numpy as np
import math

# ---------------- HELPER FUNCTIONS ----------------

# Convert a character to number (A=0 ... Z=25)
def char_to_num(c):
    return ord(c.upper()) - ord('A')

# Convert number to character
def num_to_char(n):
    return chr(int(n) + ord('A'))

# Compute modular inverse of a number mod 26
def mod_inverse(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None  # No inverse

# Compute inverse of 2x2 key matrix modulo 26
def invert_key_matrix(key):
    det = int(np.round(np.linalg.det(key)))  # determinant
    det_mod = det % 26

    inv_det = mod_inverse(det_mod)
    if inv_det is None:
        return None  # matrix not invertible

    # adjugate matrix
    adj = np.array([[key[1][1], -key[0][1]],
                    [-key[1][0], key[0][0]]])

    inv_key = (inv_det * adj) % 26
    return inv_key

# ---------------- HILL ENCRYPTION ----------------
def hill_encrypt(plaintext, key):
    plaintext = plaintext.replace(" ", "").upper()

    # Pad if odd length
    if len(plaintext) % 2 != 0:
        plaintext += 'X'

    ciphertext = ""
    for i in range(0, len(plaintext), 2):
        block = np.array([[char_to_num(plaintext[i])],
                          [char_to_num(plaintext[i+1])]])
        result = np.dot(key, block) % 26
        ciphertext += num_to_char(result[0][0]) + num_to_char(result[1][0])

    return ciphertext

# ---------------- HILL DECRYPTION ----------------
def hill_decrypt(ciphertext, key):
    # Pad ciphertext if odd length
    if len(ciphertext) % 2 != 0:
        print("Warning: Ciphertext length is odd. Adding 'X' for decryption.")
        ciphertext += 'X'

    inv_key = invert_key_matrix(key)
    if inv_key is None:
        return "ERROR: Key matrix not invertible modulo 26!"

    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        first = char_to_num(ciphertext[i])
        second = char_to_num(ciphertext[i+1])
        block = np.array([[first], [second]])
        result = np.dot(inv_key, block) % 26
        plaintext += num_to_char(result[0][0]) + num_to_char(result[1][0])

    return plaintext

# ---------------- MAIN MENU ----------------
def main():
    print("==== HILL CIPHER (2x2) ====")

    # Take key matrix input with validation
    while True:
        try:
            print("\nEnter 2x2 Key Matrix (only integers):")
            a = int(input("Enter a11: "))
            b = int(input("Enter a12: "))
            c = int(input("Enter a21: "))
            d = int(input("Enter a22: "))
            key = np.array([[a, b], [c, d]])

            # Check determinant coprime with 26
            det = int(np.round(np.linalg.det(key))) % 26
            if math.gcd(det, 26) != 1:
                print("ERROR: Key matrix determinant not coprime with 26! Enter a valid key.\n")
                continue
            break
        except ValueError:
            print("Invalid input! Please enter integers only.\n")

    print("\nKey Matrix is valid and ready for use!")

    while True:
        print("\n-------- MENU --------")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        print("-----------------------")

        choice = input("Enter choice: ")

        if choice == "1":
            pt = input("Enter plaintext: ").upper()
            ct = hill_encrypt(pt, key)
            print("Ciphertext:", ct)

        elif choice == "2":
            ct = input("Enter ciphertext: ").upper()
            pt = hill_decrypt(ct, key)
            print("Plaintext:", pt)

        elif choice == "3":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Try again.")

# Run Program
main()
