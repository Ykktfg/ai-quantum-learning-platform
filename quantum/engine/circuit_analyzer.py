from __future__ import annotations

from typing import Any

from qiskit import QuantumCircuit


def analyze_circuit(circuit: QuantumCircuit) -> dict[str, Any]:
    """Analyze a quantum circuit and return educational metadata."""

    gate_counts: dict[str, int] = {}

    for instruction in circuit.data:
        gate_name = instruction.operation.name.upper()

        gate_counts[gate_name] = gate_counts.get(gate_name, 0) + 1

    total_gates = sum(gate_counts.values())

    has_superposition = any(
        gate in gate_counts
        for gate in {"H", "RX", "RY", "SX"}
    )

    has_entanglement = any(
        gate in gate_counts
        for gate in {"CX", "CY", "CZ", "CH", "CCX"}
    )

    if has_entanglement:
        explanation = (
            "This circuit contains multi-qubit controlled operations "
            "that can create or manipulate entanglement."
        )
    elif has_superposition:
        explanation = (
            "This circuit contains operations that can create "
            "quantum superposition."
        )
    else:
        explanation = (
            "This circuit primarily performs single-qubit operations "
            "without an obvious entangling operation."
        )

    return {
        "num_qubits": circuit.num_qubits,
        "num_classical_bits": circuit.num_clbits,
        "depth": circuit.depth(),
        "total_gates": total_gates,
        "gate_counts": gate_counts,
        "has_superposition": has_superposition,
        "has_entanglement": has_entanglement,
        "explanation": explanation,
    }