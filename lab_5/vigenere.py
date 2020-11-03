def encrypt_char(char, key, operation=True):
    # It is assumed that BOTH CHAR and KEY have the same case (UPPER/LOWER)

    # If OPERATION is TRUE we encrypt. IF FALSE we decrypt

    lower_alphabet = "abcdefghijklmnopqrstuvwxyz"
    upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if char.islower():
        alphabet = lower_alphabet
        key = key.lower()
    else:
        alphabet = upper_alphabet
        key = key.upper()

    if char not in alphabet:
        return char

    char_index = alphabet.index(char)

    key_index = alphabet.index(key)

    # If char is not in alphabet e.g. (" ", "!!@#!@$%^")

    if operation:
        new_index = (char_index + key_index) % 26
    else:
        new_index = (char_index - key_index) % 26

    new_char = alphabet[new_index]

    return new_char


def match_keyword(input_len, keyword):
    if input_len > len(keyword):

        diff = input_len - len(keyword)
        x = diff // len(keyword) + 1
        y = input_len - len(keyword) * x
        keyword = (keyword * x) + keyword[:y]

    return keyword


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = list()

    keyword = match_keyword(len(plaintext), keyword)

    for original_char, keyword_char in zip(plaintext, keyword):
        new_char = encrypt_char(original_char, keyword_char)
        ciphertext.append(new_char)

    return "".join(ciphertext)


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = list()

    keyword = match_keyword(len(ciphertext), keyword)

    for original_char, keyword_char in zip(ciphertext, keyword):
        new_char = encrypt_char(original_char, keyword_char, False)
        plaintext.append(new_char)

    return "".join(plaintext)


if __name__ == "__main__":

    word = "PROGRAM"
    secret = "DOG"

    encrypted = encrypt_vigenere(word, secret)
    decrypted = decrypt_vigenere(encrypted, secret)
    print(
        f"Input: {word} | Secret: {secret} | Encrypted: {encrypted} | Decrypted: {decrypted}"
    )
