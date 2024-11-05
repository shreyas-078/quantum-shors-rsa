import random
import math
from sympy import isprime

# Generate a random odd number with the specified number of digits.
def generate_prime_candidate(digits):
    lower_bound = 10 ** (digits - 1)
    upper_bound = 10 ** digits
    return random.randint(lower_bound, upper_bound) | 1  # Ensure it's odd, even numbers can't be prime.

# Generate a prime number with a specified number of digits.
def generate_prime(digits):
    while True:
        candidate = generate_prime_candidate(digits)
        if isprime(candidate):
            return candidate

# Find a coprime of phi.
def find_coprime(phi):
    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    return e

# Generates a pair of RSA keys (public and private) with the given number of digits.
def generate_rsa_keys(n):
    p = generate_prime(n)  # Generate an n-digit prime
    q = generate_prime(n)  # Generate another n-digit prime
    while p == q:  # Ensure p and q are distinct
        q = generate_prime(n)

    N = p * q
    phi = (p - 1) * (q - 1)

    e = find_coprime(phi)
    d = pow(e, -1, phi)  # Compute the modular inverse of e mod phi

    return (N, e), (N, d), p, q  # (public_key, private_key, p, q)
