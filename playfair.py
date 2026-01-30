import string

def generate_matrix(key):
    key = key.lower()
    key = ''.join(ch for ch in key if ch.isalpha())
    key = key.replace('j', 'i')

    matrix = []
    used = set()

    for ch in key:
        if ch not in used:
            used.add(ch)
            matrix.append(ch)

    for ch in string.ascii_lowercase:
        if ch != 'j' and ch not in used:
            matrix.append(ch)

    return [matrix[i:i+5] for i in range(0, 25, 5)]


def find_pos(matrix, ch):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j


def get_space_positions(text):
    return [i for i, ch in enumerate(text) if ch == ' ']


def restore_spaces(text, space_pos):
    for pos in space_pos:
        text = text[:pos] + ' ' + text[pos:]
    return text


def prepare_text(text):
    text = text.lower()
    text = text.replace('j', 'i')
    text = ''.join(ch for ch in text if ch.isalpha())

    result = ""
    i = 0

    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else ''

        if a == b:
            result += a + 'x'
            i += 1
        else:
            result += a + b
            i += 2

    if len(result) % 2 != 0:
        result += 'x'

    return result


def encrypt(plaintext, matrix):
    spaces = get_space_positions(plaintext)
    prepared = prepare_text(plaintext)

    print("\nPrepared Text :", prepared)
    print("\nEncryption Steps:")

    cipher = ""

    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i+1]
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)

        if r1 == r2:
            ca = matrix[r1][(c1 + 1) % 5]
            cb = matrix[r2][(c2 + 1) % 5]
            rule = "Same Row"
        elif c1 == c2:
            ca = matrix[(r1 + 1) % 5][c1]
            cb = matrix[(r2 + 1) % 5][c2]
            rule = "Same Column"
        else:
            ca = matrix[r1][c2]
            cb = matrix[r2][c1]
            rule = "Rectangle"

        cipher += ca + cb
        print(f"{a}{b} -> {ca}{cb}  ({rule})")

    return cipher.upper(), spaces


def remove_padding_x(text):
    result = ""
    i = 0
    while i < len(text):
        if i+2 < len(text) and text[i] == text[i+2] and text[i+1] == 'x':
            result += text[i]
            i += 2
        else:
            result += text[i]
            i += 1

    if result.endswith('x'):
        result = result[:-1]

    return result


def decrypt(ciphertext, matrix, spaces):
    ciphertext = ciphertext.lower()
    print("\nDecryption Steps:")
    plain = ""

    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)

        if r1 == r2:
            pa = matrix[r1][(c1 - 1) % 5]
            pb = matrix[r2][(c2 - 1) % 5]
            rule = "Same Row"
        elif c1 == c2:
            pa = matrix[(r1 - 1) % 5][c1]
            pb = matrix[(r2 - 1) % 5][c2]
            rule = "Same Column"
        else:
            pa = matrix[r1][c2]
            pb = matrix[r2][c1]
            rule = "Rectangle"

        plain += pa + pb
        print(f"{a}{b} -> {pa}{pb}  ({rule})")

    plain = remove_padding_x(plain)
    plain = restore_spaces(plain, spaces)

    return plain


key = input("Enter key: ")
matrix = generate_matrix(key)

print("\nPlayfair Matrix:")
for row in matrix:
    print(row)

plaintext = input("\nEnter plaintext: ")

cipher, space_positions = encrypt(plaintext, matrix)
print("\nEncrypted Text:", cipher)

decrypted = decrypt(cipher, matrix, space_positions)
print("\nFinal Decrypted Text:", decrypted)
