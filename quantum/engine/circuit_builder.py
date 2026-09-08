from __future__ import annotations

from typing import Any

from qiskit import QuantumCircuit


SUPPORTED_GATES = {
    "I",
    "H",
    "X",
    "Y",
    "Z",
    "S",
    "T",
    "SX",
    "RX",
    "RY",
    "RZ",
    "CX",
    "CY",
    "CZ",
    "CH",
    "SWAP",
    "CCX",
}


def validate_gate(gate: dict[str, Any], num_qubits: int) -> None:
    """Validate a single gate before adding it to the circuit."""

    gate_name = gate.get("gate", "").upper()

    if gate_name not in SUPPORTED_GATES:
        raise ValueError(f"Unsupported gate: {gate_name}")

    # Single-qubit gates
    if gate_name in {
        "I", "H", "X", "Y", "Z", "S", "T", "SX",
        "RX", "RY", "RZ"
    }:
        if "qubit" not in gate:
            raise ValueError(f"{gate_name} gate requires a qubit")

        qubit = gate["qubit"]

        if not isinstance(qubit, int) or not 0 <= qubit < num_qubits:
            raise ValueError(f"Invalid qubit index: {qubit}")

    # Two-qubit gates
    elif gate_name in {"CX", "CY", "CZ", "CH", "SWAP"}:
        if "control" not in gate or "target" not in gate:
            raise ValueError(
                f"{gate_name} gate requires control and target qubits"
            )

        control = gate["control"]
        target = gate["target"]

        if not isinstance(control, int) or not 0 <= control < num_qubits:
            raise ValueError(f"Invalid control qubit index: {control}")

        if not isinstance(target, int) or not 0 <= target < num_qubits:
            raise ValueError(f"Invalid target qubit index: {target}")

        if control == target:
            raise ValueError(
                "Control and target qubits must be different"
            )

    # Three-qubit gate
    elif gate_name == "CCX":
        for key in ("control1", "control2", "target"):
            if key not in gate:
                raise ValueError(
                    "CCX gate requires control1, control2, and target"
                )

        control1 = gate["control1"]
        control2 = gate["control2"]
        target = gate["target"]

        for name, qubit in [
            ("control1", control1),
            ("control2", control2),
            ("target", target),
        ]:
            if not isinstance(qubit, int) or not 0 <= qubit < num_qubits:
                raise ValueError(
                    f"Invalid {name} qubit index: {qubit}"
                )

        if len({control1, control2, target}) != 3:
            raise ValueError(
                "CCX control and target qubits must all be different"
            )


def build_circuit(
    num_qubits: int,
    gates: list[dict[str, Any]],
) -> QuantumCircuit:
    """Build a Qiskit circuit from frontend gate data."""

    if not isinstance(num_qubits, int) or num_qubits < 1:
        raise ValueError("num_qubits must be at least 1")

    qc = QuantumCircuit(num_qubits, num_qubits)

    for gate in gates:
        validate_gate(gate, num_qubits)

        gate_name = gate["gate"].upper()

        if gate_name == "I":
            qc.id(gate["qubit"])

        elif gate_name == "H":
            qc.h(gate["qubit"])

        elif gate_name == "X":
            qc.x(gate["qubit"])

        elif gate_name == "Y":
            qc.y(gate["qubit"])

        elif gate_name == "Z":
            qc.z(gate["qubit"])

        elif gate_name == "S":
            qc.s(gate["qubit"])

        elif gate_name == "T":
            qc.t(gate["qubit"])

        elif gate_name == "SX":
            qc.sx(gate["qubit"])

        elif gate_name == "RX":
            qc.rx(gate["angle"], gate["qubit"])

        elif gate_name == "RY":
            qc.ry(gate["angle"], gate["qubit"])

        elif gate_name == "RZ":
            qc.rz(gate["angle"], gate["qubit"])

        elif gate_name == "CX":
            qc.cx(gate["control"], gate["target"])

        elif gate_name == "CY":
            qc.cy(gate["control"], gate["target"])

        elif gate_name == "CZ":
            qc.cz(gate["control"], gate["target"])

        elif gate_name == "CH":
            qc.ch(gate["control"], gate["target"])

        elif gate_name == "SWAP":
            qc.swap(gate["control"], gate["target"])

        elif gate_name == "CCX":
            qc.ccx(
                gate["control1"],
                gate["control2"],
                gate["target"],
            )

    qc.measure(range(num_qubits), range(num_qubits))

    return qc