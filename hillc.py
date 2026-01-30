import numpy as np
def mod_inverse(a, m):
    a = a % m
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None
def matrix_mod_inverse(K, m=26):
    det = int(round(np.linalg.det(K)))
    det_mod = det % m
    det_inv = mod_inverse(det_mod, m)
    if det_inv is None:
        return None, det, det_mod, det_inv
    K_inv_real = np.linalg.inv(K)
    adj = np.rint(det * K_inv_real).astype(int)
    K_inv_mod = (det_inv * adj) % m
    return K_inv_mod, det, det_mod, det_inv
print("*** HILL CIPHER (ENCRYPTION + DECRYPTION) ***")
raw_plain = input("Enter the plain text: ")
# decide case based on letters only (ignore spaces/punctuations)
letters_only = "".join(ch for ch in raw_plain if ch.isalpha())
keep_lower = letters_only.islower() and letters_only != ""
plain_text = raw_plain.replace(" ", "").upper()
n = int(input("Enter key size n (e.g., 2 or 3): "))
print(f"Enter {n}x{n} matrix as key (each row space-separated):")
c = []
for i in range(n):
    row = list(map(int, input().split()))
    if len(row) != n:
        raise ValueError(f"Row {i+1} must contain exactly {n} numbers.")
    c.append(row)
K = np.array(c, dtype=int) % 26
# ---------- ENCRYPTION ----------
orig_len = len(plain_text)  # letters length before padding
r = len(plain_text) % n
pad_len = 0
if r != 0:
    pad_len = n - r
    plain_text += "X" * pad_len
plain_vec = np.array([ord(ch) - 65 for ch in plain_text], dtype=int)
P = plain_vec.reshape(-1, n)
C_before_mod = P @ K
C = C_before_mod % 26
cipher_text = "".join(chr(int(x) + 65) for x in C.flatten())
# outputs in same case style as input
cipher_out = cipher_text.lower() if keep_lower else cipher_text
plain_out_with_pad = plain_text.lower() if keep_lower else plain_text
print("\n ENCRYPTION ")
print("Key K:\n", K)
print("Plain Text (with padding):", plain_out_with_pad)
print("Plain Text Matrix:\n", P)
print("After multiplication (Before mod 26):\n", C_before_mod)
print("Cipher Text Matrix (After mod 26):\n", C)
print("Cipher Text:", cipher_out)
# ---------- DECRYPTION ----------
K_inv_mod, det, det_mod, det_inv = matrix_mod_inverse(K, 26)
print("det(K) =", det)
print("det(K) mod 26 =", det_mod)
if K_inv_mod is None:
    print("No modular inverse for det(K) mod 26, so K is NOT invertible mod 26.")
    print("Decryption not possible with this key.")
else:
    print("Inverse of det(K) mod 26 =", det_inv)
    print("K inverse (mod 26):\n", K_inv_mod)
    cipher_vec = np.array([ord(ch) - 65 for ch in cipher_text], dtype=int)
    Cmat = cipher_vec.reshape(-1, n)
    P_before_mod_dec = Cmat @ K_inv_mod
    P_dec = P_before_mod_dec % 26
    decrypted_with_padding = "".join(chr(int(x) + 65) for x in P_dec.flatten())
    decrypted_no_padding = decrypted_with_padding[:orig_len]
    dec_out_pad = decrypted_with_padding.lower() if keep_lower else decrypted_with_padding
    dec_out = decrypted_no_padding.lower() if keep_lower else decrypted_no_padding
    print("\n DECRYPTION ")
    print("Cipher Text Matrix:\n", Cmat)
    print("After multiplication with K_inv (Before mod 26):\n", P_before_mod_dec)
    print("Plain Text Matrix (After mod 26):\n", P_dec)
    print("Decrypted Text (with padding):", dec_out_pad)
    print("Decrypted Text (original length):", dec_out)