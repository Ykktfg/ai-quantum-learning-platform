import json
import uuid
from typing import Any

from app.services.quantum_client import quantum_client


class SimulationService:
    """
    Backend simulation service.

    The backend does not execute the quantum circuit itself.
    It sends the circuit to the Quantum team's API through
    quantum_client and normalizes the response for the backend.
    """

    SUPPORTED_BACKENDS = {
        "qiskit",
        "aer",
    }

    # ========================================================
    # SUBMIT SIMULATION
    # ========================================================

    def submit_simulation(
        self,
        circuit_id: int,
        circuit_data: str,
        backend: str,
        shots: int,
    ) -> dict[str, Any]:
        """
        Send a stored circuit to the Quantum team's API.

        The Quantum API performs the actual quantum simulation.
        This service converts the Quantum response into the
        response format expected by the backend.
        """

        # ----------------------------------------------------
        # Validate circuit ID
        # ----------------------------------------------------

        if circuit_id <= 0:
            raise ValueError(
                "Circuit ID must be greater than 0"
            )

        # ----------------------------------------------------
        # Validate backend
        # ----------------------------------------------------

        backend = backend.lower().strip()

        if backend not in self.SUPPORTED_BACKENDS:
            raise ValueError(
                f"Unsupported simulation backend: {backend}"
            )

        # ----------------------------------------------------
        # Validate shots
        # ----------------------------------------------------

        if shots < 1:
            raise ValueError(
                "Shots must be at least 1"
            )

        if shots > 100000:
            raise ValueError(
                "Shots cannot exceed 100000"
            )

        # ----------------------------------------------------
        # Parse circuit JSON
        # ----------------------------------------------------

        try:
            data = json.loads(circuit_data)

        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError(
                "Invalid circuit data"
            ) from exc

        if not isinstance(data, dict):
            raise ValueError(
                "Circuit data must be an object"
            )

        # ----------------------------------------------------
        # Validate number of qubits
        # ----------------------------------------------------

        qubits = data.get("qubits")

        if not isinstance(qubits, int):
            raise ValueError(
                "Circuit must contain a valid integer 'qubits'"
            )

        if qubits < 1:
            raise ValueError(
                "Circuit must contain at least one qubit"
            )

        if qubits > 20:
            raise ValueError(
                "Circuit cannot contain more than 20 qubits"
            )

        # ----------------------------------------------------
        # Validate gates
        # ----------------------------------------------------

        gates = data.get("gates", [])

        if not isinstance(gates, list):
            raise ValueError(
                "Circuit 'gates' must be a list"
            )

        # ----------------------------------------------------
        # Send circuit to Quantum API
        # ----------------------------------------------------

        try:
            quantum_result = quantum_client.simulate(
                circuit_data=data,
                shots=shots,
            )

        except ValueError:
            raise

        except RuntimeError as exc:
            raise RuntimeError(
                f"Quantum simulation service unavailable: {exc}"
            ) from exc

        # ----------------------------------------------------
        # Validate Quantum API response
        # ----------------------------------------------------

        if not isinstance(quantum_result, dict):
            raise RuntimeError(
                "Quantum API returned an invalid response"
            )

        # ----------------------------------------------------
        # Extract simulation result
        # ----------------------------------------------------

        simulation = quantum_result.get(
            "simulation",
            {}
        )

        if not isinstance(simulation, dict):
            raise RuntimeError(
                "Quantum API returned an invalid simulation result"
            )

        counts = simulation.get(
            "counts",
            {}
        )

        if not isinstance(counts, dict):
            raise RuntimeError(
                "Quantum API returned invalid measurement counts"
            )

        returned_shots = simulation.get(
            "shots",
            shots
        )

        # ----------------------------------------------------
        # Generate backend job ID
        # ----------------------------------------------------

        job_id = (
            f"job-{uuid.uuid4().hex[:12]}"
        )

        # ----------------------------------------------------
        # Return normalized backend response
        # ----------------------------------------------------

        return {
            "job_id": job_id,
            "circuit_id": circuit_id,
            "backend": backend,
            "shots": returned_shots,
            "status": "completed",
            "counts": counts,

            # Keep the richer Quantum API response available
            # for future AI/analytics integration.
            "quantum_result": quantum_result,
        }


# ============================================================
# SINGLE SERVICE INSTANCE
# ============================================================


    def simulate_direct(
        self,
        circuit_data: str | dict[str, Any],
        backend: str = "qiskit",
        shots: int = 1024,
    ) -> dict[str, Any]:
        """Run a transient simulation without creating a database record."""

        if backend not in self.SUPPORTED_BACKENDS:
            raise ValueError(
                f"Unsupported simulation backend: {backend}. "
                f"Supported backends: {sorted(self.SUPPORTED_BACKENDS)}"
            )

        if not isinstance(shots, int) or shots < 1 or shots > 100000:
            raise ValueError("Shots must be between 1 and 100000")

        if isinstance(circuit_data, str):
            try:
                data = json.loads(circuit_data)
            except json.JSONDecodeError as exc:
                raise ValueError("Invalid circuit data") from exc
        else:
            data = circuit_data

        if not isinstance(data, dict):
            raise ValueError("Circuit data must be an object")

        qubits = data.get("qubits")

        if not isinstance(qubits, int):
            raise ValueError("Circuit must contain a valid integer 'qubits'")

        if qubits < 1 or qubits > 20:
            raise ValueError("Circuit qubits must be between 1 and 20")

        gates = data.get("gates", [])

        if not isinstance(gates, list):
            raise ValueError("Circuit 'gates' must be a list")

        try:
            quantum_result = quantum_client.simulate(
                circuit_data=data,
                shots=shots,
            )
        except ValueError:
            raise
        except RuntimeError as exc:
            raise RuntimeError(
                f"Quantum simulation service unavailable: {exc}"
            ) from exc

        if not isinstance(quantum_result, dict):
            raise RuntimeError("Quantum API returned an invalid response")

        simulation = quantum_result.get("simulation", {})

        if not isinstance(simulation, dict):
            raise RuntimeError(
                "Quantum API returned an invalid simulation response"
            )

        counts = simulation.get("counts", {})

        if not isinstance(counts, dict):
            counts = {}

        return {
            "counts": counts,
            "shots": simulation.get("shots", shots),
            "num_qubits": simulation.get("num_qubits", qubits),
            "depth": simulation.get("depth", 0),
            "size": simulation.get("size", len(gates)),
            "statevector": simulation.get(
                "statevector",
                simulation.get("state", []),
            ),
            "circuit": simulation.get("circuit", ""),
        }

simulation_service = SimulationService()
