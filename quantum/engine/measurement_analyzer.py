from __future__ import annotations

import math
from typing import Any


def analyze_measurements(
    counts: dict[str, int],
    shots: int,
    tolerance: float = 0.05,
) -> dict[str, Any]:
    """
    Analyze measurement counts from a quantum circuit.

    Provides probabilities, dominant states, entropy,
    distribution classification, and an educational interpretation.
    """

    if shots < 1:
        raise ValueError("shots must be at least 1")

    if not counts:
        return {
            "total_shots": shots,
            "observed_states": [],
            "most_likely_state": None,
            "most_likely_probability": 0.0,
            "entropy": 0.0,
            "distribution": "no_results",
            "interpretation": "No measurement results were observed.",
        }

    total_counts = sum(counts.values())

    if total_counts != shots:
        raise ValueError(
            f"Measurement counts ({total_counts}) "
            f"do not match shots ({shots})"
        )

    probabilities = {
        state: count / shots
        for state, count in counts.items()
    }

    sorted_states = sorted(
        probabilities.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    most_likely_state, most_likely_probability = sorted_states[0]

    # Shannon entropy.
    entropy = 0.0

    for probability in probabilities.values():
        if probability > 0:
            entropy -= probability * math.log2(probability)

    observed_states = list(probabilities.keys())

    if len(observed_states) == 1:
        distribution = "deterministic"

        interpretation = (
            f"The circuit produced the state "
            f"|{most_likely_state}> in every observed shot."
        )

    elif len(observed_states) == 2:
        values = list(probabilities.values())

        if abs(values[0] - values[1]) <= tolerance:
            distribution = "approximately_uniform"

            interpretation = (
                "The measurements are approximately evenly distributed "
                "between the observed states."
            )
        else:
            distribution = "biased"

            interpretation = (
                f"The state |{most_likely_state}> was observed most often, "
                f"with probability approximately "
                f"{most_likely_probability:.3f}."
            )

    else:
        maximum_probability = 1 / len(observed_states)

        if all(
            abs(probability - maximum_probability) <= tolerance
            for probability in probabilities.values()
        ):
            distribution = "approximately_uniform"
            interpretation = (
                "The observed states have approximately similar "
                "measurement probabilities."
            )
        else:
            distribution = "multi_state_biased"
            interpretation = (
                f"The circuit produced {len(observed_states)} different "
                f"observed states with different probabilities."
            )

    return {
        "total_shots": shots,
        "observed_states": observed_states,
        "probabilities": probabilities,
        "most_likely_state": most_likely_state,
        "most_likely_probability": most_likely_probability,
        "entropy": entropy,
        "distribution": distribution,
        "interpretation": interpretation,
    }