import struct

def md5(message):
    """
    MD5 hash implementation with step tracking for intermediate values.
    Returns: (hash_hex, steps_dict)
    """
    
    steps = {
        "input_length": 0,
        "padded_length": 0,
        "initial_state": {},
        "blocks": [],
        "rounds": []
    }
    
    # Convert message to bytes if string
    if isinstance(message, str):
        msg_bytes = message.encode('utf-8')
    else:
        msg_bytes = message
    
    input_length = len(msg_bytes)
    steps["input_length"] = input_length
    steps["message"] = message if isinstance(message, str) else msg_bytes.decode('utf-8', errors='replace')
    
    # MD5 constants
    T = [0 for _ in range(64)]
    for i in range(64):
        T[i] = int(abs(2**32 * __import__('math').sin(i + 1))) & 0xffffffff
    
    # MD5 Initial values
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476
    
    steps["initial_state"] = {
        "A": format(A, '08x'),
        "B": format(B, '08x'),
        "C": format(C, '08x'),
        "D": format(D, '08x')
    }
    
    # Padding
    msg_bit_len = input_length * 8
    msg = bytearray(msg_bytes)
    msg.append(0x80)
    
    while (len(msg) % 64) != 56:
        msg.append(0x00)
    
    # Append length (little-endian)
    msg.extend(struct.pack('<Q', msg_bit_len))
    
    steps["padded_length"] = len(msg)
    
    # Process each 512-bit block
    for offset in range(0, len(msg), 64):
        block = msg[offset:offset+64]
        steps["blocks"].append(block.hex())
        
        # Parse block into 16 32-bit words (little-endian)
        X = list(struct.unpack('<16I', block))
        
        # Save initial values for this block
        AA = A
        BB = B
        CC = C
        DD = D
        
        # 64 rounds
        round_steps = []
        
        for i in range(64):
            if i < 16:
                F = (B & C) | ((~B) & D)
                g = i
            elif i < 32:
                F = (D & B) | ((~D) & C)
                g = (5 * i + 1) % 16
            elif i < 48:
                F = B ^ C ^ D
                g = (3 * i + 5) % 16
            else:
                F = C ^ (B | (~D))
                g = (7 * i) % 16
            
            s_values = [
                7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
                5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
                4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
                6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
            ]
            
            s = s_values[i]
            temp = (A + F + T[i] + X[g]) & 0xffffffff
            temp = ((temp << s) | (temp >> (32 - s))) & 0xffffffff
            temp = (temp + B) & 0xffffffff
            
            A = D
            D = C
            C = B
            B = temp
            
            # Store selected round values
            if i % 8 == 0 or i == 63:
                round_steps.append({
                    "round": i,
                    "A": format(A, '08x'),
                    "B": format(B, '08x'),
                    "C": format(C, '08x'),
                    "D": format(D, '08x')
                })
        
        steps["rounds"].extend(round_steps)
        
        # Add block result
        A = (A + AA) & 0xffffffff
        B = (B + BB) & 0xffffffff
        C = (C + CC) & 0xffffffff
        D = (D + DD) & 0xffffffff
    
    # Final hash (little-endian representation)
    hash_bytes = struct.pack('<4I', A, B, C, D)
    hash_hex = hash_bytes.hex()
    
    steps["final_state"] = {
        "A": format(A, '08x'),
        "B": format(B, '08x'),
        "C": format(C, '08x'),
        "D": format(D, '08x')
    }
    
    return hash_hex, steps


if __name__ == "__main__":
    print("===== MD5 Hash =====")
    
    message = input("Enter message: ")
    
    hash_result, steps = md5(message)
    
    print(f"\nInput length: {steps['input_length']} bytes")
    print(f"Padded length: {steps['padded_length']} bytes")
    print(f"\nInitial State:")
    print(f"  A: {steps['initial_state']['A']}")
    print(f"  B: {steps['initial_state']['B']}")
    print(f"  C: {steps['initial_state']['C']}")
    print(f"  D: {steps['initial_state']['D']}")
    print(f"\nFinal MD5: {hash_result}")
