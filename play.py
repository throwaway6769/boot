def prepare_text(text):
    """Remove spaces, punctuation and convert to uppercase, handle double letters"""
    text = text.upper()
    cleaned = ""
    i = 0
    while i < len(text):
        if text[i].isalpha():
            cleaned += text[i]
            if i < len(text)-1 and text[i] == text[i+1]:
                cleaned += 'X'  # Insert X between double letters
                i += 1
            else:
                i += 1
        else:
            i += 1
    
    # If odd length, add X at the end
    if len(cleaned) % 2 == 1:
        cleaned += 'X'
    
    return cleaned

def generate_playfair_matrix(key):
    """Generate 5x5 Playfair matrix from key (I/J combined)"""
    key = key.upper()
    matrix = []
    used = set()
    
    # Add key letters first
    for char in key:
        if char.isalpha() and char not in used:
            if char == 'J':
                char = 'I'  # Treat J as I
            if char not in used:
                matrix.append(char)
                used.add(char)
    
    # Add remaining alphabet (skip J)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in used:
            matrix.append(ch)
            used.add(ch)
    
    # Convert to 5x5 grid
    playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
    return playfair_matrix

def find_position(matrix, letter):
    """Find row and column of a letter in the matrix"""
    if letter == 'J':
        letter = 'I'
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col
    return None

def playfair_encrypt(plaintext, key):
    matrix = generate_playfair_matrix(key)
    text = prepare_text(plaintext)
    
    ciphertext = ""
    i = 0
    while i < len(text):
        letter1 = text[i]
        letter2 = text[i+1]
        
        row1, col1 = find_position(matrix, letter1)
        row2, col2 = find_position(matrix, letter2)
        
        if row1 == row2:  # Same row
            ciphertext += matrix[row1][(col1 + 1) % 5]
            ciphertext += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:  # Same column
            ciphertext += matrix[(row1 + 1) % 5][col1]
            ciphertext += matrix[(row2 + 1) % 5][col2]
        else:  # Rectangle rule
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]
        
        i += 2
    
    return ciphertext

def playfair_decrypt(ciphertext, key):
    matrix = generate_playfair_matrix(key)
    text = ciphertext.upper().replace(" ", "")
    
    plaintext = ""
    i = 0
    while i < len(text):
        letter1 = text[i]
        letter2 = text[i+1]
        
        row1, col1 = find_position(matrix, letter1)
        row2, col2 = find_position(matrix, letter2)
        
        if row1 == row2:  # Same row
            plaintext += matrix[row1][(col1 - 1) % 5]
            plaintext += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:  # Same column
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:  # Rectangle rule
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]
        
        i += 2
    
    # Remove padding X's where appropriate
    result = ""
    i = 0
    while i < len(plaintext):
        result += plaintext[i]
        if (i+2 < len(plaintext) and 
            plaintext[i+1] == 'X' and 
            plaintext[i] == plaintext[i+2]):
            i += 2
        else:
            i += 1
            
    return result

def print_matrix(matrix):
    print("\nPlayfair Matrix:")
    for row in matrix:
        print(" ".join(row))
    print()

def main():
    print("=== PLAYFAIR CIPHER ===")
    key = input("Enter the key (alphabets only): ").strip()
    
    while True:
        print("\n--- MENU ---")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Show Playfair Matrix")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            plaintext = input("Enter plaintext: ")
            matrix = generate_playfair_matrix(key)
            ciphertext = playfair_encrypt(plaintext, key)
            print(f"Encrypted Text: {ciphertext}")
            
        elif choice == '2':
            ciphertext = input("Enter ciphertext: ")
            plaintext = playfair_decrypt(ciphertext, key)
            print(f"Decrypted Text: {plaintext}")
            
        elif choice == '3':
            matrix = generate_playfair_matrix(key)
            print_matrix(matrix)
            
        elif choice == '4':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()