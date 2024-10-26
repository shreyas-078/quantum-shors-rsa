# Implementation of Shor's algorithm for quantum factorization.
# Could be used to break RSA encryption, with enogh perfect Qubits.
# This implementation does not guarantee precision results for smaller numbers itself, let alone huge N values.
# It only serves as a demonstration for how a Shor's algorithm would normally be implemented.

import numpy as np
import math
import random
import pennylane as qml


def find_coprime(N):
    a = random.randint(2, N - 1)
    while math.gcd(a, N) != 1:  # Continue until co-prime is found
        a = random.randint(2, N - 1)
    return a


def qft(wires):
    for i in range(len(wires)):
        qml.Hadamard(wires=i)  # Create superposition on every qubit
        for j in range(i + 1, len(wires)):
            qml.ctrl(
                qml.PhaseShift(np.pi / 2 ** (j - i), wires=j), control=i
            )  # Apply phase shift


def inv_qft(wires):
    for i in reversed(range(len(wires))):
        for j in reversed(range(i + 1, len(wires))):
            qml.ctrl(
                qml.PhaseShift(-np.pi / 2 ** (j - i), wires=j), control=i
            )  # Reverse the phase shift
        qml.Hadamard(wires=i)  # Reverse Hadamard transformation


def q_find_order(a, N, qubits=8, shots=512):  # Reduced qubits and shots
    dev = qml.device(
        "lightning.qubit", wires=qubits, shots=shots
    )  # Set up the quantum device

    a_powers = [pow(a, 2**i, N) for i in range(qubits)]  # Precompute powers of 'a' % N

    @qml.qnode(dev)
    def circuit():
        for i in range(qubits):
            qml.Hadamard(wires=i)  # Put each qubit in superposition

        for i in range(qubits):
            qml.ctrl(
                qml.PhaseShift(2 * np.pi * a_powers[i] / N, wires=(i + 1) % qubits),
                control=i,
            )  # Controlled phase shift based on powers of a

        inv_qft(
            range(qubits)
        )  # Apply inverse quantum fourier transform to retrieve the order

        return qml.sample(
            wires=range(qubits)
        )  # Sample qubits to get measurement results

    samples = circuit()  # Get samples

    measured_integer = int("".join(map(str, samples[0])), 2)
    candidate_r = measured_integer

    if candidate_r != 0 and pow(a, candidate_r, N) == 1:
        return candidate_r
    return None  # No valid order is found


def shors_algo(N):
    if N % 2 == 0:
        return [2]  # Early factor detection for even numbers

    a = find_coprime(N)

    print(
        f"Attempting to find the order of a = {a} modulo N = {N} using quantum simulation..."
    )
    r = q_find_order(a, N)

    if r is None or r % 2 != 0:
        print(
            "Quantum order finding failed. This system is unpredictable due to the current limitations of quantum technology."
        )
        return []

    # Use the order to determine the factors of N
    x1 = pow(a, r // 2, N)
    if x1 == N - 1 or x1 == 1:  # Early abort if x1 leads to trivial factorization
        return []

    f1 = math.gcd(x1 - 1, N)
    f2 = math.gcd(x1 + 1, N)

    factors = []
    if f1 != 1 and f1 != N:
        factors.append(f1)
    if f2 != 1 and f2 != N:
        factors.append(f2)

    return factors if factors else []


# Testing the implementation
if __name__ == "__main__":
    N = 27221
    print(f"Attempting to factorize N = {N}")
    factors = []
    while not factors:
        factors = shors_algo(N)
        print(
            "No factors found. This could be due to the unpredictability of quantum systems."
        )
    print(f"Factors of {N} found: {factors}")

