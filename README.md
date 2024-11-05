# Security with RSA and Quantum Computing

Using the ideas of quantum physics, quantum computing is a novel approach to computing. It is still in the experimental phase, and there are still numerous obstacles to overcome.

1. Unpredictability: Quantum systems are highly unpredictable. They rely on the properties of quantum states which are probabilistic, it might be challenging to consistently produce precise results because the results can differ between runs.
2. Perfect Qubits: A large number of perfect qubits is required for methods such as Shor's algorithm to successfully crack RSA-2048 encryption. The limitations of current quantum computers include limited qubit counts, decoherence, and high mistake rates. It is estimated that around 4,000 to 20,000 logical qubits could be required for RSA-2048 to be broken. Hence the current implementation uses a Maximum of RSA-32 as a demonstration.
3. RSA Security: Due to the limitations of modern quantum computers, RSA-2048 is currently safe from quantum attacks and considered secure against classical assaults. But RSA encryption might be in danger if powerful quantum computers become more accessible.
4. Time Estimation: RSA-2048 might be factored in a matter of seconds to minutes if we have a sufficiently strong quantum computer with the necessary number of perfect qubits. This is in contrast to the approx. 300 trillion years it would take for a classical computer to factorise current RSA standard keys.

# Shor's Algorithm for Integer Factorization

This repository contains a Python implementation of **Shor's Algorithm**, a quantum algorithm for factoring large integers efficiently. This algorithm is a cornerstone of quantum computing and has significant implications for cryptography, especially for RSA.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [How It Works](#how-it-works)
- [Testing the Implementation](#testing-the-implementation)
- [Contributing](#contributing)
- [License](#license)

## Features

- Generates RSA public and private keys.
- Finds coprime integers to facilitate quantum order finding.
- Implements Quantum Fourier Transform (QFT) and its inverse.
- Uses PennyLane for simulating quantum circuits.
- Attempts to factor a given integer using Shor's algorithm.

## Getting Started

### Prerequisites

Make sure you have Python installed on your system. This program is compatible with Python 3.x.

### Dependencies

To run this code, you will need to install the following packages:

```bash
pip install numpy sympy pennylane
```

### Cloning the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/shreyas-078/quantum-shors-rsa.git
cd quantum-shors-rsa
```

## Usage

You can run the program directly by executing the main script. By default, it attempts to factor the integer 15:

```bash
python quantum-utils.py
```

## How It Works

Shor's algorithm consists of the following key steps:

1. **RSA Key Generation**: Generates two large prime numbers and computes the public and private keys.
2. **Coprime Selection**: Randomly selects a coprime integer \(a\) for better chances of success.
3. **Quantum Order Finding**: Utilizes quantum circuits to find the order \(r\) of \(a\) modulo \(N\).
4. **Factorization**: Calculates potential factors of \(N\) based on the found order.

### Quantum Components

- **Quantum Fourier Transform (QFT)**: Transforms the quantum state to facilitate order finding.
- **Inverse QFT**: Retrieves the order from the transformed state.

## Testing the Implementation

To test the implementation, simply run the main script as described in the [Usage](#usage) section. You can modify the integer \(N\) in the code to test with different values. The program will print the factors found or indicate if no factors were discovered.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any issues, please create an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
