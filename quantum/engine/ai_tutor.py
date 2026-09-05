from __future__ import annotations

from typing import Any


def generate_tutor_response(
    question: str,
    circuit_analysis: dict[str, Any],
    state_analysis: dict[str, Any],
    measurement_analysis: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate a grounded, student-friendly explanation
    using actual circuit and simulation analysis.
    """

    question_lower = question.lower()

    concepts = []

    if circuit_analysis.get("has_superposition"):
        concepts.append("superposition")

    if circuit_analysis.get("has_entanglement"):
        concepts.append("entanglement")

    gate_counts = circuit_analysis.get("gate_counts", {})
    state_expression = state_analysis.get(
        "state_expression",
        "Unknown",
    )

    distribution = measurement_analysis.get(
        "distribution",
        "unknown",
    )

    most_likely_state = measurement_analysis.get(
        "most_likely_state",
    )

    most_likely_probability = measurement_analysis.get(
        "most_likely_probability",
        0.0,
    )

    # --------------------------------
    # ENTANGLEMENT QUESTIONS
    # --------------------------------

    if "entangle" in question_lower:

        if circuit_analysis.get("has_entanglement"):

            controlled_gates = [
                gate
                for gate in ["CX", "CY", "CZ", "CH", "CCX"]
                if gate in gate_counts
            ]

            return {
                "answer": (
                    "Your circuit can create entanglement because it "
                    "contains a multi-qubit controlled operation "
                    f"({', '.join(controlled_gates)}). "
                    "These gates make the state of one qubit depend on "
                    "another qubit. In this circuit, the final state is "
                    f"{state_expression}. "
                    "This means the qubits cannot simply be described "
                    "as independent single-qubit states."
                ),
                "concepts": ["Entanglement"],
                "evidence": {
                    "controlled_gates": controlled_gates,
                    "final_state": state_expression,
                },
            }

        return {
            "answer": (
                "I don't see an obvious entangling operation in this "
                "circuit. Multi-qubit controlled gates such as CX, CY, "
                "CZ, CH, or CCX are commonly used to create or manipulate "
                "entanglement."
            ),
            "concepts": ["Entanglement"],
            "evidence": {
                "has_entanglement": False,
            },
        }

    # --------------------------------
    # SUPERPOSITION QUESTIONS
    # --------------------------------

    if "superposition" in question_lower:

        if circuit_analysis.get("has_superposition"):

            return {
                "answer": (
                    "Your circuit contains an operation capable of "
                    "creating superposition. The resulting quantum state "
                    f"is {state_expression}. "
                    "Because more than one basis state has a non-zero "
                    "amplitude, the qubit system has multiple possible "
                    "measurement outcomes before measurement."
                ),
                "concepts": ["Superposition"],
                "evidence": {
                    "final_state": state_expression,
                    "has_superposition": True,
                },
            }

        return {
            "answer": (
                "This circuit does not contain an obvious operation "
                "that creates superposition."
            ),
            "concepts": ["Superposition"],
            "evidence": {
                "has_superposition": False,
            },
        }

    # --------------------------------
    # PROBABILITY QUESTIONS
    # --------------------------------

    if (
        "probability" in question_lower
        or "chance" in question_lower
        or "50/50" in question_lower
    ):

        return {
            "answer": (
                f"The most frequently observed state was "
                f"|{most_likely_state}> with an observed probability "
                f"of approximately {most_likely_probability:.3f}. "
                f"The measurement distribution was classified as "
                f"'{distribution}'. "
                "Measurement probabilities come from the squared "
                "magnitudes of the quantum state's amplitudes."
            ),
            "concepts": ["Measurement", "Probability"],
            "evidence": {
                "most_likely_state": most_likely_state,
                "most_likely_probability": most_likely_probability,
                "distribution": distribution,
            },
        }

    # --------------------------------
    # GATE QUESTIONS
    # --------------------------------

    if "gate" in question_lower or "h gate" in question_lower:

        return {
            "answer": (
                "The circuit contains the following gates: "
                f"{gate_counts}. "
                "Each gate transforms the quantum state. "
                "For example, an H gate can create superposition, "
                "while controlled gates can create or manipulate "
                "relationships between qubits."
            ),
            "concepts": concepts,
            "evidence": {
                "gate_counts": gate_counts,
            },
        }

    # --------------------------------
    # GENERAL QUESTION
    # --------------------------------

    return {
        "answer": (
            "Based on your circuit, I found "
            f"{circuit_analysis.get('num_qubits', 0)} qubits and "
            f"{circuit_analysis.get('total_gates', 0)} gates. "
            f"The final quantum state is {state_expression}. "
            f"The measurement distribution is '{distribution}'. "
            "Ask me specifically about superposition, entanglement, "
            "probabilities, gates, or the final state and I can explain "
            "that part in more detail."
        ),
        "concepts": concepts,
        "evidence": {
            "num_qubits": circuit_analysis.get("num_qubits"),
            "total_gates": circuit_analysis.get("total_gates"),
            "gate_counts": gate_counts,
            "final_state": state_expression,
            "distribution": distribution,
        },
    }