from __future__ import annotations

from typing import Any
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector


class QuantumSimulator:
    """Common simulation interface for the learning platform."""

    def __init__(self) -> None:
        self.backend = AerSimulator()

    def run(self, circuit: QuantumCircuit, shots: int = 1000) -> dict[str, Any]:
        """Run a measured circuit and return counts plus useful metadata."""
        compiled = transpile(circuit, self.backend)
        result = self.backend.run(compiled, shots=shots).result()
        counts = result.get_counts()

        # Convert measurement counts into probabilities.
        probabilities = {
            state: count / shots
            for state, count in counts.items()
        }

        return {
            "counts": dict(counts),
            "probabilities": probabilities,
            "shots": shots,
            "num_qubits": circuit.num_qubits,
            "depth": circuit.depth(),
            "size": circuit.size(),
        }

    @staticmethod
    def statevector(circuit: QuantumCircuit) -> list[dict[str, float]]:
        """Return statevector amplitudes as JSON-friendly real/imag pairs."""
        # Statevector simulation requires a circuit without final measurements.
        clean = circuit.remove_final_measurements(inplace=False)
        state = Statevector.from_instruction(clean)

        return [
            {
                "real": float(amplitude.real),
                "imag": float(amplitude.imag),
            }
            for amplitude in state.data
        ]
