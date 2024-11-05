import pennylane as qml
import numpy as np
import math
import time
import random
import itertools
from rsa_keygen import generate_rsa_keys

prime_number_digits = 5 # Number of digits used for the prime numbers used to calculate N (Max tested: 5)
add_delay = True # If you want to add artifical delay for classical method

# Set Up a Quantum device setup with 6 qubits
dev = qml.device("default.qubit", wires=6, shots=1024)

# Finds a co-prime of N.
def find_coprime(N):
    a = random.randint(2, N - 1)
    while math.gcd(a, N) != 1:
        a = random.randint(2, N - 1)
    return a

# Controlled modular exponentiation circuit for Shor's algorithm.
def controlled_modular_exponentiation(a, N, exponent, target_wire):
    base = pow(a, 2 ** exponent, N)
    qml.PhaseShift(2 * np.pi * base / N, wires=target_wire)

# Quantum Phase Estimation to find order r of a modulo N."""
def quantum_phase_estimation(a, N, num_qubits=5):
    @qml.qnode(dev)
    def circuit():
        # Initialize each qubit in superposition
        for i in range(num_qubits):
            qml.Hadamard(wires=i)

        # Apply controlled modular exponentiation
        for i in range(num_qubits):
            controlled_modular_exponentiation(a, N, i, target_wire=i)

        # Apply Inverse Quantum Fourier Transform
        inv_qft(range(num_qubits))
        return qml.probs(wires=range(num_qubits))

    # Execute the circuit and return the most probable measurement outcome
    probability_distribution = circuit()
    measured_integer = np.argmax(probability_distribution)
    return measured_integer

# Applies the inverse Quantum Fourier Transform.
def inv_qft(wires):
    for i in reversed(range(len(wires))):
        for j in reversed(range(i)):
            qml.ctrl(qml.PhaseShift(-np.pi / 2 ** (i - j), wires=i), control=j)
        qml.Hadamard(wires=i)

# Shor's factorization algorithm using quantum simulation.
def shors_factorization(N):
    a = find_coprime(N)
    print(f"Selected co-prime a = {a}")

    # Run quantum phase estimation to find the order r
    r = quantum_phase_estimation(a, N)
    if r is None or r % 2 != 0:
        return None  # Return None if quantum factorization fails

    # Calculate potential factors based on the order
    x1 = pow(a, int(r) // 2, N)  # Ensure r is a plain integer
    if x1 == N - 1 or x1 == 1:
        return None  # Return None if trivial factors are found

    f1 = math.gcd(x1 - 1, N)
    f2 = math.gcd(x1 + 1, N)
    factors = [factor for factor in (f1, f2) if factor != 1 and factor != N]
    
    return factors if factors else None

# Simulates realistic workload for classical factorization.
# Simulated workload for classical factorization
def simulate_classical_delay(iterations):
    # Introduce a simulated workload based on the number of iterations
    for i in range(iterations):
        _ = sum(itertools.islice(itertools.count(), i)) # Multiple Parallel processes introduce higher computational load
        time.sleep(0.001)

# Classical factorization for comparison
def classical_factorization(N):
    """Brute-force classical factorization for benchmarking."""
    for i in range(2, int(np.sqrt(N)) + 1):
        if(add_delay):
            simulate_classical_delay(i)  # Introduce a workload before checking divisibility
        if N % i == 0:
            return [i, N // i]
    return []

# Demonstration
if __name__ == "__main__":
    public_key, private_key, p, q = generate_rsa_keys(prime_number_digits)
    N = public_key[0] # RSA modulus
    print(f"Attempting to factorize N = {N} using Shor's algorithm...")

    quantum_factors = None
    attempt_count = 0
    start_time = time.time()

    # Repeat until quantum factorization succeeds
    while not quantum_factors:
        attempt_count += 1
        quantum_factors = shors_factorization(N)
        if quantum_factors:
            quantum_factors.append(N//quantum_factors[0])
            quantum_time = time.time() - start_time
            print(f"\nQuantum factors of {N} found: {quantum_factors} in {quantum_time:.4f} seconds after {attempt_count} attempts.")
        else:
            print(f"Attempt {attempt_count}: Quantum factorization failed. Retrying...")

    # Classical benchmarking for comparison
    print("\nAttempting classical factorization...")
    start_time = time.time()
    classical_factors = classical_factorization(N)
    classical_time = time.time() - start_time
    print(f"Classical factors of {N} found: {classical_factors} in {classical_time:.4f} seconds.")

    # Compare results
    if quantum_factors:
        print(f"\nQuantum method took {quantum_time:.4f} seconds vs. Classical {classical_time:.4f} seconds.")
        speedup = classical_time / quantum_time if quantum_time > 0 else float('inf')
        print(f"Speedup factor (Quantum over Classical): {speedup:.2f}x")
