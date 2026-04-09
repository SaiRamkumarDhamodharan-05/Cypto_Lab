print("=== Diffie-Hellman Key Exchange (With Steps) ===")

# Step 1: Public values
p = int(input("Enter prime number p: "))
g = int(input("Enter base g: "))

print("\nSTEP 1: Public values")
print("p =", p)
print("g =", g)

# Step 2: Private keys
a = int(input("\nEnter Alice private key a: "))
b = int(input("Enter Bob private key b: "))

print("\nSTEP 2: Private keys")
print("Alice private key a =", a)
print("Bob private key b   =", b)

# Step 3: Public key generation
A = (g ** a) % p
B = (g ** b) % p

print("\nSTEP 3: Generate public keys")
print(f"Alice public key A = (g^a) mod p = ({g}^{a}) mod {p} = {A}")
print(f"Bob public key B   = (g^b) mod p = ({g}^{b}) mod {p} = {B}")

# Step 4: Exchange public keys
print("\nSTEP 4: Exchange public keys")
print("Alice sends A to Bob:", A)
print("Bob sends B to Alice:", B)

# Step 5: Shared secret generation
alice_secret = (B ** a) % p
bob_secret = (A ** b) % p

print("\nSTEP 5: Generate shared secret")
print(f"Alice computes: (B^a) mod p = ({B}^{a}) mod {p} = {alice_secret}")
print(f"Bob computes:   (A^b) mod p = ({A}^{b}) mod {p} = {bob_secret}")

# Step 6: Verify
print("\nSTEP 6: Verify")
if alice_secret == bob_secret:
    print("Success: Both secret keys are same.")
    print("Shared Secret Key =", alice_secret)
else:
    print("Error: Secret keys are different.")