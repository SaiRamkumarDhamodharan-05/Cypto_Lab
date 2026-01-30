import random
import math
def euclidean_primality(n):
    print("\n--- Euclidean Method (GCD-based) ---")
    is_prime = True
    if n < 2:
        print("No numbers >1 to test. Not prime.")
        return False
    for i in range(2, n):
        g = math.gcd(n, i)
        print(f"gcd({n}, {i}) = {g}")
        if g > 1:
            is_prime = False
    return is_prime

def fermat_primality(n, k=3):
    print("\n--- Fermat Primality Test ---")

    if n < 4:
        print(f"No valid 'a' exists for n = {n} (range 2 to n-2 is empty).")
        print("Algorithm cannot proceed.")
        return n > 1

    is_prime = True
    for t in range(1, k + 1):
        a = random.randint(2, n - 2)
        value = pow(a, n - 1, n)
        print(f"Trial {t}: a = {a}")
        print(f"{a}^{n-1} mod {n} = {value}")
        if value != 1:
            is_prime = False
    return is_prime
def miller_rabin_primality(n, k=3):
    print("\n--- Miller–Rabin Primality Test ---")

    if n < 4:
        print(f"n - 1 = {n-1} × 2^0")
        print("No valid random base 'a' exists.")
        print("Algorithm cannot proceed.")
        return n > 1

    # Write n-1 = d * 2^r
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    print(f"n - 1 = {d} × 2^{r}")

    is_prime = True
    for t in range(1, k + 1):
        a = random.randint(2, n - 2)
        print(f"\nTrial {t}: a = {a}")
        x = pow(a, d, n)
        print(f"x = {a}^{d} mod {n} = {x}")

        if x == 1 or x == n - 1:
            print("Passed initial condition")
            continue

        witness_found = True
        for i in range(r - 1):
            x = pow(x, 2, n)
            print(f"x squared = {x}")
            if x == n - 1:
                witness_found = False
                break

        if witness_found:
            print("Witness found -> composite")
            is_prime = False
    return is_prime
def main():
    try:
        n = int(input("Enter number to test primality: "))
    except ValueError:
        print("Invalid input! Please enter an integer.")
        return

    print("\nChoose Method:")
    print("1. Euclidean Method")
    print("2. Fermat Test")
    print("3. Miller–Rabin Test")

    choice = input("Enter choice (1/2/3): ")

    if choice == "1":
        result = euclidean_primality(n)
        method = "Euclidean Method"
    elif choice == "2":
        result = fermat_primality(n)
        method = "Fermat Test"
    elif choice == "3":
        result = miller_rabin_primality(n)
        method = "Miller–Rabin Test"
    else:
        print("Invalid choice!")
        return

    print(f"\nResult using {method}:")
    if result:
        print(f"{n} is PRIME")
    else:
        print(f"{n} is NOT PRIME")


if __name__ == "__main__":
    main()
