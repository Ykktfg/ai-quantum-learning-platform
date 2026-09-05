from __future__ import annotations


GATE_EXPLANATIONS = {
    "I": {
        "name": "Identity",
        "type": "single-qubit",
        "qubits": 1,
        "parameterized": False,
        "concepts": ["Identity operation"],
        "description": "Leaves the qubit unchanged.",
        "educational": (
            "The Identity gate does not change the quantum state. "
            "It is useful for representing an intentional delay or "
            "an unchanged qubit."
        ),
    },

    "H": {
        "name": "Hadamard",
        "type": "single-qubit",
        "qubits": 1,
        "parameterized": False,
        "concepts": ["Superposition"],
        "description": "Creates an equal superposition of |0> and |1>.",
        "educational": (
            "The Hadamard gate transforms |0> into "
            "(|0> + |1>) / sqrt(2), creating superposition. "
            "It is one of the most important gates for quantum algorithms."
        ),
    },

    "X": {
        "name": "Pauli-X",
        "type": "single-qubit",
        "qubits": 1,
        "parameterized": False,
        "concepts": ["Bit flip"],
        "description": "Flips |0> to |1> and |1> to |0>.",
        "educational": (
            "The X gate is the quantum equivalent of a classical NOT gate. "
            "It flips the computational basis state of a qubit."
        ),
    },

    "Y": {
        "name": "Pauli-Y",
        "type": "single-qubit",
        "qubits": 1,
        "parameterized": False,
        "concepts": ["Bit flip", "Phase"],
        "description": "Performs a bit flip combined with a phase change.",
        "educational": (
            "The Y gate changes the computational state while also "
            "introducing a phase factor."
        ),
    },

    "Z": {
        "name": "Pauli-Z",
        "type": "single-qubit",
        "qubits": 1,
        "parameterized": False,
        "concepts": ["Phase"],
        "description": "Applies a phase flip to the |1> component.",
        "educational": (
            "The Z gate leaves |0> unchanged but changes the phase of "
            "the |1> component by multiplying it by -1."
        ),
    },

    "S": {
        "name": "S Gate",
        "type": "single-qubit",
        "qubits": 1,
        "parameterized": False,
        "concepts": ["Phase"],
        "description": "Applies a pi/2 phase rotation.",
        "educational": (
            "The S gate applies a 90-degree phase rotation to the |1> "
            "component of a qubit."
        ),
    },

    "T": {
        "name": "T Gate",
        "type": "single-qubit",
        "qubits": 1,
        "parameterized": False,
        "concepts": ["Phase"],
        "description": "Applies a pi/4 phase rotation.",
        "educational": (
            "The T gate applies a 45-degree phase rotation to the |1> "
            "component of a qubit."
        ),
    },

    "SX": {
        "name": "Square-Root of X",
        "type": "single-qubit",
        "qubits": 1,
        "parameterized": False,
        "concepts": ["Superposition", "Rotation"],
        "description": "Applies the square root of the X operation.",
        "educational": (
            "The SX gate performs an operation whose square is equivalent "
            "to an X gate. It can create superposition from computational "
            "basis states."
        ),
    },

    "RX": {
        "name": "X Rotation",
        "type": "single-qubit",
        "qubits": 1,
        "parameterized": True,
        "parameter": "angle",
        "concepts": ["Rotation", "Superposition"],
        "description": "Rotates the qubit around the X axis.",
        "educational": (
            "The RX gate rotates a qubit around the X axis of the Bloch "
            "sphere. The amount of rotation is controlled by the angle."
        ),
    },

    "RY": {
        "name": "Y Rotation",
        "type": "single-qubit",
        "qubits": 1,
        "parameterized": True,
        "parameter": "angle",
        "concepts": ["Rotation", "Superposition"],
        "description": "Rotates the qubit around the Y axis.",
        "educational": (
            "The RY gate rotates a qubit around the Y axis of the Bloch "
            "sphere. Different angles produce different superpositions."
        ),
    },

    "RZ": {
        "name": "Z Rotation",
        "type": "single-qubit",
        "qubits": 1,
        "parameterized": True,
        "parameter": "angle",
        "concepts": ["Rotation", "Phase"],
        "description": "Rotates the qubit around the Z axis.",
        "educational": (
            "The RZ gate rotates a qubit around the Z axis. It changes "
            "the relative phase of the quantum state."
        ),
    },

    "CX": {
        "name": "Controlled-X (CNOT)",
        "type": "two-qubit",
        "qubits": 2,
        "parameterized": False,
        "concepts": ["Entanglement", "Controlled operation"],
        "description": (
            "Applies X to the target when the control qubit is |1>."
        ),
        "educational": (
            "The CX, or CNOT, gate uses one qubit as a control and another "
            "as a target. It is fundamental for creating and manipulating "
            "entanglement."
        ),
    },

    "CY": {
        "name": "Controlled-Y",
        "type": "two-qubit",
        "qubits": 2,
        "parameterized": False,
        "concepts": ["Entanglement", "Controlled operation"],
        "description": "Applies Y to the target when the control is |1>.",
        "educational": (
            "The CY gate applies a Y operation to the target qubit only "
            "when the control qubit is in the |1> state."
        ),
    },

    "CZ": {
        "name": "Controlled-Z",
        "type": "two-qubit",
        "qubits": 2,
        "parameterized": False,
        "concepts": ["Entanglement", "Phase", "Controlled operation"],
        "description": "Applies a Z operation conditionally.",
        "educational": (
            "The CZ gate applies a phase flip when both relevant qubits "
            "are in the |1> state. It is commonly used in entangling circuits."
        ),
    },

    "CH": {
        "name": "Controlled-Hadamard",
        "type": "two-qubit",
        "qubits": 2,
        "parameterized": False,
        "concepts": ["Superposition", "Controlled operation"],
        "description": "Applies H to the target when the control is |1>.",
        "educational": (
            "The CH gate conditionally applies a Hadamard operation to "
            "the target qubit based on the control qubit."
        ),
    },

    "SWAP": {
        "name": "SWAP",
        "type": "two-qubit",
        "qubits": 2,
        "parameterized": False,
        "concepts": ["Qubit exchange"],
        "description": "Exchanges the states of two qubits.",
        "educational": (
            "The SWAP gate exchanges the quantum states of two qubits. "
            "It does not by itself create entanglement."
        ),
    },

    "CCX": {
        "name": "Toffoli / Controlled-Controlled-X",
        "type": "three-qubit",
        "qubits": 3,
        "parameterized": False,
        "concepts": ["Controlled operation", "Reversible computing"],
        "description": (
            "Applies X to the target when both control qubits are |1>."
        ),
        "educational": (
            "The CCX gate, also called the Toffoli gate, has two control "
            "qubits and one target. The target is flipped only when both "
            "controls are in the |1> state."
        ),
    },
}


def get_gate_info(gate_name: str) -> dict:
    """Return educational information about a supported gate."""
    gate_name = gate_name.upper()

    if gate_name not in GATE_EXPLANATIONS:
        raise ValueError(f"Unsupported gate: {gate_name}")

    return GATE_EXPLANATIONS[gate_name]


def get_all_gate_info() -> dict:
    """Return the complete gate knowledge base."""
    return GATE_EXPLANATIONS