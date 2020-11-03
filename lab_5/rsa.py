import random


def gcd_extended(e, phi):
    if e == 0:
        return (phi, 0, 1)
    else:
        div, x, y = gcd_extended(phi % e, e)
    return (y - (phi // e) * x) % phi, y - (phi // e) * x, x


def multiplicative_inverse(e: int, phi: int) -> int:
    """
    >>> multiplicative_inverse(7, 40)
    23
    """

    _, d, _ = gcd_extended(e, phi)

    return d % phi


def gcd(x, y):
    if y == 0:
        return x
    else:
        return gcd(y, x % y)


def is_prime(n: int) -> bool:
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """

    if n <= 1:
        return False

    if n <= 3:

        return True

    end = int(n ** 0.5) + 1

    for i in range(2, end):
        if n % i == 0:
            return False

    return True


def generate_keypair(p: int, q: int):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be equal")

    # n = pq
    n = p * q

    # phi = (p-1)(q-1)
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))
