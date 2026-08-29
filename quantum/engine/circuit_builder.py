from __future__ import annotations

from typing import Any
from qiskit import QuantumCircuit


def build_circuit(
    num_qubits: int,
    gates: list[dict[str, Any]],
) -> QuantumCircuit:
    """Build a Qiskit circuit from frontend-friendly gate definitions."""

    if num_qubits < 1:
        raise ValueError("num_qubits must be at least 1")

    qc = QuantumCircuit(num_qubits, num_qubits)

    for gate_data in gates:
        gate = gate_data["gate"].upper()

        # -----------------------------
        # Single-qubit gates
        # -----------------------------
        if gate in {"H", "X", "Y", "Z", "S", "T"}:
            qubit = gate_data["qubit"]

            if not 0 <= qubit < num_qubits:
                raise ValueError(f"Invalid qubit index: {qubit}")

            if gate == "H":
                qc.h(qubit)
            elif gate == "X":
                qc.x(qubit)
            elif gate == "Y":
                qc.y(qubit)
            elif gate == "Z":
                qc.z(qubit)
            elif gate == "S":
                qc.s(qubit)
            elif gate == "T":
                qc.t(qubit)

        # -----------------------------
        # Rotation gates
        # -----------------------------
        elif gate in {"RX", "RY", "RZ"}:
            qubit = gate_data["qubit"]
            angle = gate_data["angle"]

            if not 0 <= qubit < num_qubits:
                raise ValueError(f"Invalid qubit index: {qubit}")

            if gate == "RX":
                qc.rx(angle, qubit)
            elif gate == "RY":
                qc.ry(angle, qubit)
            elif gate == "RZ":
                qc.rz(angle, qubit)

        # -----------------------------
        # Controlled gates
        # -----------------------------
        elif gate in {"CX", "CZ"}:
            control = gate_data["control"]
            target = gate_data["target"]

            if not 0 <= control < num_qubits:
                raise ValueError(f"Invalid control qubit: {control}")

            if not 0 <= target < num_qubits:
                raise ValueError(f"Invalid target qubit: {target}")

            if control == target:
                raise ValueError(
                    "Control and target qubits must be different"
                )

            if gate == "CX":
                qc.cx(control, target)
            elif gate == "CZ":
                qc.cz(control, target)

        # -----------------------------
        # SWAP gate
        # -----------------------------
        elif gate == "SWAP":
            qubit1 = gate_data["qubit1"]
            qubit2 = gate_data["qubit2"]

            if not 0 <= qubit1 < num_qubits:
                raise ValueError(f"Invalid qubit index: {qubit1}")

            if not 0 <= qubit2 < num_qubits:
                raise ValueError(f"Invalid qubit index: {qubit2}")

            if qubit1 == qubit2:
                raise ValueError(
                    "SWAP requires two different qubits"
                )

            qc.swap(qubit1, qubit2)

        # -----------------------------
        # Unsupported gate
        # -----------------------------
        else:
            raise ValueError(f"Unsupported gate: {gate}")

    # Add measurements at the end
    qc.measure(
        range(num_qubits),
        range(num_qubits)
    )

    return qc