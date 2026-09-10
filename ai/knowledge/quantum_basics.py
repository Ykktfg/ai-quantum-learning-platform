QUANTUM_KNOWLEDGE = [
    {
        "topic": "qubit",
        "title": "What is a Qubit?",
        "content": """
A qubit is the basic unit of quantum information.

A classical bit can have only one of two values:
0 or 1.

A qubit can exist in a quantum state represented as:

|psi> = alpha|0> + beta|1>

where alpha and beta are complex probability amplitudes.

The probabilities of measuring 0 or 1 are:

P(0) = |alpha|^2
P(1) = |beta|^2

The probabilities must satisfy:

|alpha|^2 + |beta|^2 = 1.

A qubit should not be thought of simply as being both 0 and 1.
Instead, its state is described by a quantum superposition until measurement.
"""
    },

    {
        "topic": "superposition",
        "title": "Quantum Superposition",
        "content": """
Superposition means that a quantum system can be described as a combination
of multiple basis states.

For a single qubit:

|psi> = alpha|0> + beta|1>

The Hadamard gate is commonly used to create an equal superposition:

H|0> = (|0> + |1>) / sqrt(2)

After measurement, the result is either 0 or 1.

For an ideal measurement of this state:

P(0) = 1/2
P(1) = 1/2.
"""
    },

    {
        "topic": "measurement",
        "title": "Quantum Measurement",
        "content": """
Measurement converts quantum information into a classical result.

For a qubit in the state:

|psi> = alpha|0> + beta|1>

the probability of measuring 0 is:

|alpha|^2

and the probability of measuring 1 is:

|beta|^2.

Measurement generally changes the quantum state because it projects the state
onto the observed measurement outcome.
"""
    },

    {
        "topic": "hadamard",
        "title": "Hadamard Gate",
        "content": """
The Hadamard gate, written as H, is one of the most important quantum gates.

Its matrix is:

H = 1/sqrt(2) [[1, 1],
                [1, -1]]

Important transformations include:

H|0> = (|0> + |1>) / sqrt(2)

H|1> = (|0> - |1>) / sqrt(2)

The Hadamard gate is commonly used to create superposition.
"""
    },

    {
        "topic": "pauli_x",
        "title": "Pauli-X Gate",
        "content": """
The Pauli-X gate is similar to a classical NOT operation.

It swaps the computational basis states:

X|0> = |1>

X|1> = |0>

Its matrix is:

X = [[0, 1],
     [1, 0]]
"""
    },

    {
        "topic": "pauli_y",
        "title": "Pauli-Y Gate",
        "content": """
The Pauli-Y gate is a single-qubit quantum gate that combines a bit flip
with a phase change.

Its matrix is:

Y = [[0, -i],
     [i,  0]]
"""
    },

    {
        "topic": "pauli_z",
        "title": "Pauli-Z Gate",
        "content": """
The Pauli-Z gate changes the phase of the |1> state while leaving |0>
unchanged.

Z|0> = |0>

Z|1> = -|1>

Its matrix is:

Z = [[1,  0],
     [0, -1]]
"""
    },

    {
        "topic": "cnot",
        "title": "CNOT Gate",
        "content": """
The controlled-NOT gate, or CNOT, is a two-qubit gate.

It has a control qubit and a target qubit.

The target qubit is flipped only when the control qubit is |1>.

For computational basis states:

|00> -> |00>
|01> -> |01>
|10> -> |11>
|11> -> |10>

CNOT is fundamental for creating and manipulating entanglement.
"""
    },

    {
        "topic": "entanglement",
        "title": "Quantum Entanglement",
        "content": """
Entanglement is a quantum correlation in which the joint state of multiple
qubits cannot be represented as independent states of the individual qubits.

A common example is the Bell state:

|Phi+> = (|00> + |11>) / sqrt(2)

When this state is measured in the computational basis, the outcomes 00
and 11 occur with equal probability in the ideal case.

Entanglement is an important resource in quantum communication,
quantum algorithms, and quantum information processing.
"""
    },

    {
        "topic": "bell_state",
        "title": "Bell State Circuit",
        "content": """
A common circuit for creating the Bell state |Phi+> is:

1. Start with two qubits in |00>.
2. Apply a Hadamard gate to qubit 0.
3. Apply a CNOT with qubit 0 as control and qubit 1 as target.

The resulting state is:

(|00> + |11>) / sqrt(2)

An ideal computational-basis measurement produces only 00 and 11,
with equal probabilities.
"""
    },

    {
        "topic": "ghz_state",
        "title": "GHZ State",
        "content": """
A GHZ state is a multi-qubit entangled state.

For three qubits, a common GHZ state is:

(|000> + |111>) / sqrt(2)

A circuit can create it by:

1. Applying H to the first qubit.
2. Applying CNOT from qubit 0 to qubit 1.
3. Applying CNOT from qubit 1 to qubit 2.

Ideal computational-basis measurement produces 000 or 111
with equal probability.
"""
    },

    {
        "topic": "quantum_circuit",
        "title": "Quantum Circuits",
        "content": """
A quantum circuit represents a sequence of operations performed on qubits.

A typical circuit contains:

- Quantum registers
- Classical registers
- Quantum gates
- Measurements

Gates transform quantum states.
Measurements produce classical information.

Circuit depth represents the length of the longest sequence of dependent
operations in the circuit.
"""
    }
]
