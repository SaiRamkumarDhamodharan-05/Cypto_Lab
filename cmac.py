from Crypto.Cipher import AES

BLOCK_SIZE = 16
Rb = 0x87

def print_block(label, b):
    print(f"{label}: {b.hex()}")

def left_shift(block):
    shifted = int.from_bytes(block, 'big') << 1
    return (shifted & (2**128 - 1)).to_bytes(16, 'big')

def generate_subkeys(key, debug=False):
    if debug:
        print("\n--- Subkey Generation ---")
    cipher = AES.new(key, AES.MODE_ECB)

    L = cipher.encrypt(b'\x00' * BLOCK_SIZE)
    if debug:
        print_block("L", L)

    if (L[0] & 0x80) == 0:
        K1 = left_shift(L)
    else:
        K1 = (int.from_bytes(left_shift(L), 'big') ^ Rb).to_bytes(16, 'big')

    if debug:
        print_block("K1", K1)

    if (K1[0] & 0x80) == 0:
        K2 = left_shift(K1)
    else:
        K2 = (int.from_bytes(left_shift(K1), 'big') ^ Rb).to_bytes(16, 'big')

    if debug:
        print_block("K2", K2)

    return K1, K2, L

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def cmac_aes(key, message, Tlen, debug=False):
    if debug:
        print("\n================ CMAC START ================")
    
    cipher = AES.new(key, AES.MODE_ECB)
    K1, K2, L = generate_subkeys(key, debug)
    
    steps = {
        "L": L.hex(),
        "K1": K1.hex(),
        "K2": K2.hex(),
        "blocks": [],
        "cbc_steps": []
    }

    if debug:
        print("\n--- Block Division ---")
    
    n = (len(message) + BLOCK_SIZE - 1) // BLOCK_SIZE

    if n == 0:
        n = 1
        flag = False
    else:
        flag = (len(message) % BLOCK_SIZE == 0)

    blocks = [message[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE] for i in range(n)]

    for i, blk in enumerate(blocks):
        if debug:
            print_block(f"M{i+1}", blk)
        steps["blocks"].append(blk.hex())

    if debug:
        print("\n--- Last Block ---")
    
    if flag:
        last_block = xor_bytes(blocks[-1], K1)
    else:
        padded = blocks[-1] + b'\x80' + b'\x00' * (BLOCK_SIZE - len(blocks[-1]) - 1)
        if debug:
            print_block("Padded", padded)
        last_block = xor_bytes(padded, K2)

    if debug:
        print_block("FinalBlock", last_block)
    
    steps["last_block"] = last_block.hex()

    if debug:
        print("\n--- CBC Processing ---")
    
    X = b'\x00' * BLOCK_SIZE
    if debug:
        print_block("X0", X)

    for i in range(n - 1):
        temp = xor_bytes(X, blocks[i])
        if debug:
            print_block(f"X⊕M{i+1}", temp)
        X = cipher.encrypt(temp)
        if debug:
            print_block(f"C{i+1}", X)
        steps["cbc_steps"].append({
            "block": i+1,
            "xor_result": temp.hex(),
            "output": X.hex()
        })

    if debug:
        print("\n--- Final ---")
    
    temp = xor_bytes(X, last_block)
    if debug:
        print_block("X⊕Last", temp)

    T = cipher.encrypt(temp)
    if debug:
        print_block("TagFull", T)
        print_block(f"Tag({Tlen})", T[:Tlen])
        print("\n================ CMAC END ================")

    # Add final block to steps
    steps["cbc_steps"].append({
        "block": "Final",
        "xor_result": temp.hex(),
        "output": T.hex()
    })

    steps["final_xor"] = temp.hex()
    steps["tag_full"] = T.hex()
    steps["tag"] = T[:Tlen].hex()

    return T[:Tlen], steps

if __name__ == "__main__":
    print("===== CMAC using AES =====")

    key_input = input("Enter key (max 16 chars): ").encode()
    message_input = input("Enter message: ").encode()
    Tlen = int(input("Enter tag length (1-16): "))

    if Tlen < 1 or Tlen > 16:
        print("Invalid Tlen")
        exit()

    key = key_input.ljust(16, b'\x00')[:16]

    tag, steps = cmac_aes(key, message_input, Tlen, debug=True)

    print("\nFINAL TAG:", tag.hex())
