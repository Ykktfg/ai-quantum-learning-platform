from __future__ import annotations

import math
from typing import Any


def analyze_statevector(
    statevector: list[dict[str, float]],
    num_qubits: int,
    tolerance: float = 1e-10,
) -> dict[str, Any]:
    """
    Analyze a JSON-friendly quantum statevector.

    Returns non-zero basis states, probabilities,
    normalization information, and a readable expression.
    """

    expected_length = 2 ** num_qubits

    if len(statevector) != expected_length:
        raise ValueError(
            f"Statevector length must be {expected_length} "
            f"for {num_qubits} qubits"
        )

    nonzero_states = []
    total_probability = 0.0

    for index, amplitude_data in enumerate(statevector):
        real = float(amplitude_data.get("real", 0.0))
        imag = float(amplitude_data.get("imag", 0.0))

        magnitude_squared = real ** 2 + imag ** 2
        total_probability += magnitude_squared

        if magnitude_squared <= tolerance:
            continue

        basis_state = format(index, f"0{num_qubits}b")
        magnitude = math.sqrt(magnitude_squared)

        phase = math.atan2(imag, real)

        nonzero_states.append(
            {
                "state": basis_state,
                "amplitude": {
                    "real": real,
                    "imag": imag,
                },
                "magnitude": magnitude,
                "probability": magnitude_squared,
                "phase_radians": phase,
            }
        )

    nonzero_states.sort(
        key=lambda item: item["probability"],
        reverse=True,
    )

    probabilities = {
        item["state"]: item["probability"]
        for item in nonzero_states
    }

    is_normalized = math.isclose(
        total_probability,
        1.0,
        abs_tol=1e-8,
    )

    has_superposition = len(nonzero_states) > 1

    expression_terms = []

    for item in nonzero_states:
        real = item["amplitude"]["real"]
        imag = item["amplitude"]["imag"]
        state = item["state"]

        if abs(imag) <= tolerance:
            expression_terms.append(
                f"{real:.4f}|{state}>"
            )
        else:
            expression_terms.append(
                f"({real:.4f} + {imag:.4f}i)|{state}>"
            )

    expression = " + ".join(expression_terms)

    return {
        "num_qubits": num_qubits,
        "dimension": expected_length,
        "nonzero_states": nonzero_states,
        "probabilities": probabilities,
        "total_probability": total_probability,
        "is_normalized": is_normalized,
        "has_superposition": has_superposition,
        "state_expression": expression,
    }