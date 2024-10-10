# Classical approach to break RSA encryption.
# Very inefficient as packets reach the sender before the decryption is complete.

import time


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def classical_rsa_break(n):
    start_time = time.time()
    for i in range(2, n):
        if n % i == 0:
            p, q = i, n // i
            break
    end_time = time.time()
    return p, q, end_time - start_time


n = 3233  # RSA modulus
p, q, duration = classical_rsa_break(n)
print(f"Classical approach: p = {p}, q = {q}, Time taken = {duration} seconds")
