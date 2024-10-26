# Classical approach to break RSA encryption.
# Very inefficient as packets reach the sender before the decryption is complete.

import time


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def classical_rsa_break(n):
    start_time = time.time()

    # Loop to find the first divisor of n, starting from 2
    for i in range(2, int(n**0.5) + 1):  # Only iterate up to sqrt(n) for efficiency
        if n % i == 0:
            p, q = i, n // i
            end_time = time.time()
            return p, q, end_time - start_time  # Return p, q and the duration of the process

    end_time = time.time()
    return None, None, end_time - start_time  # No factors found (for prime n)


n = 27221  # RSA modulus
p, q, duration = classical_rsa_break(n)

if p and q:
    print(f"Classical approach: p = {p}, q = {q}, Time taken = {duration:.6f} seconds")
else:
    print(f"Failed to factorize {n}. Time taken = {duration:.6f} seconds")
