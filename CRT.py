# -------------------------------------------------------------
# Chinese Remainder Theorem Based Calculator
# Performs addition, subtraction, multiplication, division
# on large numbers using CRT representation
# -------------------------------------------------------------

from math import gcd

# -------------------------------------------------------------
# Function: Extended Euclidean Algorithm 
# Used for computing modular inverse
# -------------------------------------------------------------
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

# -------------------------------------------------------------
# Function: Modular inverse of a modulo m
# -------------------------------------------------------------
def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception(f"No modular inverse for {a} mod {m}")
    return x % m

# -------------------------------------------------------------
# Convert a large integer A into CRT tuple (a1, a2, …, ak)
# -------------------------------------------------------------
def to_crt_representation(A, mod_list):
    return [A % mi for mi in mod_list]

# -------------------------------------------------------------
# Perform operation in CRT space component-wise
# -------------------------------------------------------------
def operate_crt(a_list, b_list, mod_list, op):
    c = []
    for ai, bi, mi in zip(a_list, b_list, mod_list):

        if op == 1:          # Addition
            c.append((ai + bi) % mi)

        elif op == 2:        # Subtraction
            c.append((ai - bi) % mi)

        elif op == 3:        # Multiplication
            c.append((ai * bi) % mi)

        elif op == 4:        # Division → multiply by inverse
            bi_inv = mod_inverse(bi, mi)
            c.append((ai * bi_inv) % mi)

    return c

# -------------------------------------------------------------
# Reconstruct number from CRT tuple using standard CRT formula
# C = Σ (ci * Mi * Mi_inverse) mod M
# -------------------------------------------------------------
def reconstruct_from_crt(c_list, mod_list):
    M = 1
    for mi in mod_list:
        M *= mi

    # Compute Mi = M/mi for each
    Mi_list = [M // mi for mi in mod_list]

    # Compute inverses of Mi modulo mi
    inv_list = [mod_inverse(Mi_list[i], mod_list[i]) for i in range(len(mod_list))]

    # Apply CRT formula
    result = 0
    for i in range(len(mod_list)):
        result += c_list[i] * Mi_list[i] * inv_list[i]

    return result % M

# -------------------------------------------------------------
# Main Menu-Driven Program
# -------------------------------------------------------------
def main():
    print("------------------------------------------------------------")
    print("     Chinese Remainder Theorem - Arithmetic Calculator      ")
    print("------------------------------------------------------------")

    # Initialization: user provides moduli m1, m2, ..., mk (all coprime)
    k = int(input("Enter number of moduli k: "))
    mod_list = []
    print("Enter", k, "pairwise-coprime moduli:")
    for i in range(k):
        mod_list.append(int(input(f"m{i+1} = ")))

    # Precompute M = m1*m2*...*mk
    M = 1
    for mi in mod_list:
        M *= mi

    while True:
        print("\n------------------- Menu -------------------")
        print("1. Addition (A + B)")
        print("2. Subtraction (A - B)")
        print("3. Multiplication (A * B)")
        print("4. Division (A / B)")
        print("5. Quit")
        print("--------------------------------------------")

        op = int(input("Choose an option: "))

        if op == 5:
            print("Exiting... Goodbye!")
            break

        if op not in [1, 2, 3, 4]:
            print("Invalid choice. Try again!")
            continue

        # Take two large numbers
        A = int(input("\nEnter A: "))
        B = int(input("Enter B: "))

        # Convert A and B to CRT form
        a_list = to_crt_representation(A, mod_list)
        b_list = to_crt_representation(B, mod_list)

        print("\nA in CRT form =", a_list)
        print("B in CRT form =", b_list)

        # Perform CRT operation
        c_list = operate_crt(a_list, b_list, mod_list, op)
        print("Result in CRT form =", c_list)

        # Reconstruct actual number using CRT
        C = reconstruct_from_crt(c_list, mod_list)

        # Print final result
        print(f"\nFinal Answer C = A ? B (mod M = {M})")
        print("C =", C)
        print("--------------------------------------------")

# Run program
main()
