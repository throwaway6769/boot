def extended_euclid_with_table(a, m):
    print("\nq\t r1\t r2\t r\t t1\t t2\t t")
    print("------------------------------------------------------")

    # initial values
    r1, r2 = a, m
    t1, t2 = 1, 0

    while r2 != 0:
        q = r1 // r2
        r = r1 % r2
        t = t1 - q * t2

        print(f"{q}\t {r1}\t {r2}\t {r}\t {t1}\t {t2}\t {t}")

        # shifting
        r1, r2 = r2, r
        t1, t2 = t2, t

    gcd = r1
    mi = t1 % m if gcd == 1 else None

    print("\nResult:")
    print(f"GCD({a}, {m}) = {gcd}")
    if mi is not None:
        print(f"Multiplicative Inverse of {a} mod {m} = {mi}")
    else:
        print(f"Multiplicative Inverse does NOT exist since GCD != 1")

    return gcd, mi


# ---------------------- MAIN PROGRAM ----------------------
a = int(input("Enter value of a: "))
m = int(input("Enter modulus m: "))

extended_euclid_with_table(a, m)
