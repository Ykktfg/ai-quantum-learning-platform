from __future__ import annotations

from typing import Any

from qiskit import QuantumCircuit

from engine.gate_explanations import get_gate_info


def explain_circuit(
    circuit: QuantumCircuit,
    circuit_analysis: dict[str, Any],
    state_analysis: dict[str, Any],
    measurement_analysis: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate a student-friendly explanation of a quantum circuit.
    """

    steps: list[dict[str, Any]] = []

    step_number = 1

    for instruction in circuit.data:
        operation = instruction.operation
        gate_name = operation.name.upper()

        # Measurements are explained separately.
        if gate_name == "MEASURE":
            continue

        try:
            gate_info = get_gate_info(gate_name)
            description = gate_info["educational"]
            concepts = gate_info.get("concepts", [])
        except ValueError:
            description = f"The {gate_name} operation is applied."
            concepts = []

        qubits = [
            circuit.find_bit(qubit).index
            for qubit in instruction.qubits
        ]

        steps.append(
            {
                "step": step_number,
                "gate": gate_name,
                "qubits": qubits,
                "concepts": concepts,
                "explanation": description,
            }
        )

        step_number += 1

    concepts_detected: list[str] = []

    if circuit_analysis.get("has_superposition"):
        concepts_detected.append("Superposition")

    if circuit_analysis.get("has_entanglement"):
        concepts_detected.append("Entanglement")

    state_expression = state_analysis.get(
        "state_expression",
        "Unknown state",
    )

    distribution = measurement_analysis.get(
        "distribution",
        "unknown",
    )

    measurement_interpretation = measurement_analysis.get(
        "interpretation",
        "No measurement interpretation available.",
    )

    if circuit_analysis.get("has_entanglement"):
        summary = (
            "This circuit uses quantum operations that can create or "
            "manipulate entanglement between qubits."
        )
    elif circuit_analysis.get("has_superposition"):
        summary = (
            "This circuit creates a quantum superposition, allowing the "
            "system to contain multiple basis-state possibilities."
        )
    else:
        summary = (
            "This circuit performs quantum operations without an obvious "
            "superposition or entangling structure."
        )

    return {
        "title": "Circuit Explanation",
        "summary": summary,
        "steps": steps,
        "concepts_detected": concepts_detected,
        "final_state": state_expression,
        "measurement_distribution": distribution,
        "measurement_explanation": measurement_interpretation,
    }