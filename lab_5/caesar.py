def caesar_breaker(ciphertext: str, dictionary) -> int:
    """
    >>> d = {"python", "java", "ruby"}
    >>> caesar_breaker("python", d)
    0
    >>> caesar_breaker("sbwkrq", d)
    3
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """

    lower_alphabet = "abcdefghijklmnopqrstuvwxyz"
    upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = list()

    for char in plaintext:

        if char.islower():
            alphabet = lower_alphabet
        else:
            alphabet = upper_alphabet

        if char not in alphabet:
            result.append(char)
            continue
        char_index = alphabet.index(char)

        new_index = char_index + shift

        if new_index > 25:
            new_index = new_index % 26

        new_char = alphabet[new_index]
        result.append(new_char)

    ciphertext = "".join(result)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """

    lower_alphabet = "abcdefghijklmnopqrstuvwxyz"
    upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = list()

    for char in ciphertext:

        if char.islower():
            alphabet = lower_alphabet
        else:
            alphabet = upper_alphabet

        if char not in alphabet:
            result.append(char)
            continue

        char_index = alphabet.index(char)

        new_index = char_index + (26 - shift)

        if new_index > 25:
            new_index = new_index % 26

        new_char = alphabet[new_index]
        result.append(new_char)

    ciphertext = "".join(result)

    return ciphertext


if __name__ == "__main__":
    print(encrypt_caesar("PYTHON"))
