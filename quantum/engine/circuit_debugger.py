from __future__ import annotations

from typing import Any


def debug_circuit(
    circuit_analysis: dict[str, Any],
    state_analysis: dict[str, Any],
    measurement_analysis: dict[str, Any],
) -> dict[str, Any]:
    """
    Detect common educational issues in a quantum circuit
    and provide actionable suggestions.
    """

    issues: list[dict[str, Any]] = []
    suggestions: list[dict[str, Any]] = []

    gate_counts = circuit_analysis.get("gate_counts", {})
    num_qubits = circuit_analysis.get("num_qubits", 0)

    has_superposition = circuit_analysis.get(
        "has_superposition",
        False,
    )

    has_entanglement = circuit_analysis.get(
        "has_entanglement",
        False,
    )

    state_expression = state_analysis.get(
        "state_expression",
        "",
    )

    distribution = measurement_analysis.get(
        "distribution",
        "unknown",
    )

    # --------------------------------
    # ISSUE 1: MULTI-QUBIT CIRCUIT
    # WITHOUT ENTANGLEMENT
    # --------------------------------

    if num_qubits > 1 and not has_entanglement:

        issues.append(
            {
                "type": "missing_entanglement",
                "severity": "info",
                "message": (
                    "This circuit contains multiple qubits but "
                    "does not contain an obvious entangling operation."
                ),
                "reason": (
                    "Multi-qubit controlled gates such as CX, CY, "
                    "CZ, CH, or CCX are commonly used to create "
                    "or manipulate entanglement."
                ),
            }
        )

        suggestions.append(
            {
                "type": "add_entangling_gate",
                "message": (
                    "If your goal is to create entanglement, "
                    "try adding a CX gate between two qubits."
                ),
                "example": {
                    "gate": "CX",
                    "control": 0,
                    "target": 1,
                },
            }
        )

    # --------------------------------
    # ISSUE 2: MULTI-QUBIT CIRCUIT
    # WITHOUT SUPERPOSITION
    # --------------------------------

    if num_qubits > 1 and not has_superposition:

        issues.append(
            {
                "type": "missing_superposition",
                "severity": "info",
                "message": (
                    "The circuit does not contain an obvious "
                    "superposition-producing operation."
                ),
                "reason": (
                    "An H, RX, RY, or SX operation can create "
                    "superposition depending on the input state."
                ),
            }
        )

        suggestions.append(
            {
                "type": "add_superposition",
                "message": (
                    "Try applying an H gate to a qubit if you "
                    "want to explore superposition."
                ),
                "example": {
                    "gate": "H",
                    "qubit": 0,
                },
            }
        )

    # --------------------------------
    # ISSUE 3: CIRCUIT HAS ONLY
    # MEASUREMENT OPERATIONS
    # --------------------------------

    non_measurement_gates = (
        circuit_analysis.get("total_gates", 0)
        - gate_counts.get("MEASURE", 0)
    )

    if non_measurement_gates == 0:

        issues.append(
            {
                "type": "no_quantum_operations",
                "severity": "warning",
                "message": (
                    "The circuit contains no quantum gate operations "
                    "before measurement."
                ),
                "reason": (
                    "Without quantum operations, the qubits remain "
                    "in their initial |0> state."
                ),
            }
        )

        suggestions.append(
            {
                "type": "add_quantum_gate",
                "message": (
                    "Add a quantum gate such as X or H before "
                    "measurement to change the quantum state."
                ),
                "example": {
                    "gate": "H",
                    "qubit": 0,
                },
            }
        )

    # --------------------------------
    # ISSUE 4: DETERMINISTIC RESULT
    # --------------------------------

    if distribution == "deterministic":

        suggestions.append(
            {
                "type": "explore_probability",
                "message": (
                    "Your circuit currently produces one observed "
                    "state deterministically. Try adding an H, RX, "
                    "or RY gate to explore probabilistic outcomes."
                ),
            }
        )

    # --------------------------------
    # ISSUE 5: VERY DEEP CIRCUIT
    # --------------------------------

    depth = circuit_analysis.get("depth", 0)

    if depth > 10:

        issues.append(
            {
                "type": "high_depth",
                "severity": "warning",
                "message": (
                    f"This circuit has a depth of {depth}, "
                    "which may make it harder to understand "
                    "and potentially harder to execute on real hardware."
                ),
                "reason": (
                    "Simpler circuits are generally easier to "
                    "analyze and execute."
                ),
            }
        )

        suggestions.append(
            {
                "type": "reduce_depth",
                "message": (
                    "Consider removing unnecessary gates or "
                    "simplifying repeated operations."
                ),
            }
        )

    # --------------------------------
    # OVERALL STATUS
    # --------------------------------

    if any(
        issue["severity"] == "warning"
        for issue in issues
    ):
        status = "needs_attention"

    elif issues:
        status = "has_suggestions"

    else:
        status = "looks_good"

    # --------------------------------
    # EDUCATIONAL SUMMARY
    # --------------------------------

    if status == "looks_good":

        summary = (
            "Your circuit looks structurally reasonable based "
            "on the available analysis. No major educational "
            "issues were detected."
        )

    elif status == "has_suggestions":

        summary = (
            "Your circuit is valid, but there are some educational "
            "opportunities you may want to explore."
        )

    else:

        summary = (
            "Your circuit may need some changes. Review the "
            "detected issues and suggested improvements."
        )

    return {
        "status": status,
        "summary": summary,
        "issues": issues,
        "suggestions": suggestions,
        "state_expression": state_expression,
    }