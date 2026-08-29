import json
import uuid

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


class SimulationService:
    """
    Service responsible for executing quantum circuits
    using the Qiskit Aer simulator.
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
    ):
        """
        Parse a stored circuit, execute it using Qiskit Aer,
        and return measurement results.
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
        # Get gates
        # ----------------------------------------------------

        gates = data.get("gates", [])

        if not isinstance(gates, list):
            raise ValueError(
                "Circuit 'gates' must be a list"
            )

        # ----------------------------------------------------
        # Create Qiskit circuit
        # ----------------------------------------------------

        circuit = QuantumCircuit(
            qubits,
            qubits
        )

        # ----------------------------------------------------
        # Apply quantum gates
        # ----------------------------------------------------

        for gate in gates:

            if not isinstance(gate, dict):
                raise ValueError(
                    "Each gate must be an object"
                )

            gate_type = str(
                gate.get("type", "")
            ).upper().strip()

            target = gate.get("target")
            control = gate.get("control")

            # ------------------------------------------------
            # Validate target
            # ------------------------------------------------

            if not isinstance(target, int):
                raise ValueError(
                    f"Invalid target qubit for gate {gate_type}"
                )

            if target < 0 or target >= qubits:
                raise ValueError(
                    f"Target qubit {target} is outside "
                    f"the circuit range 0-{qubits - 1}"
                )

            # ------------------------------------------------
            # Single-qubit gates
            # ------------------------------------------------

            if gate_type == "H":

                circuit.h(target)

            elif gate_type == "X":

                circuit.x(target)

            elif gate_type == "Y":

                circuit.y(target)

            elif gate_type == "Z":

                circuit.z(target)

            elif gate_type == "S":

                circuit.s(target)

            elif gate_type == "T":

                circuit.t(target)

            # ------------------------------------------------
            # Controlled-X gate
            # ------------------------------------------------

            elif gate_type == "CX":

                if control is None:
                    raise ValueError(
                        "CX gate requires a control qubit"
                    )

                if not isinstance(control, int):
                    raise ValueError(
                        "CX control qubit must be an integer"
                    )

                if control < 0 or control >= qubits:
                    raise ValueError(
                        f"Control qubit {control} is outside "
                        f"the circuit range 0-{qubits - 1}"
                    )

                if control == target:
                    raise ValueError(
                        "Control and target qubits "
                        "cannot be the same"
                    )

                circuit.cx(
                    control,
                    target
                )

            else:

                raise ValueError(
                    f"Unsupported quantum gate: {gate_type}"
                )

        # ----------------------------------------------------
        # Add measurements
        # ----------------------------------------------------

        circuit.measure(
            range(qubits),
            range(qubits)
        )

        # ----------------------------------------------------
        # Create Aer simulator
        # ----------------------------------------------------

        simulator = AerSimulator()

        # ----------------------------------------------------
        # Transpile circuit for Aer
        # ----------------------------------------------------

        compiled_circuit = transpile(
            circuit,
            simulator
        )

        # ----------------------------------------------------
        # Execute simulation
        # ----------------------------------------------------

        job = simulator.run(
            compiled_circuit,
            shots=shots
        )

        # ----------------------------------------------------
        # Get result
        # ----------------------------------------------------

        result = job.result()

        counts = result.get_counts()

        # ----------------------------------------------------
        # Generate unique job ID
        # ----------------------------------------------------

        job_id = (
            f"job-{uuid.uuid4().hex[:12]}"
        )

        # ----------------------------------------------------
        # Return result
        # ----------------------------------------------------

        return {
            "job_id": job_id,
            "circuit_id": circuit_id,
            "backend": backend,
            "shots": shots,
            "status": "completed",
            "counts": counts,
        }


# ============================================================
# SINGLE SERVICE INSTANCE
# ============================================================

simulation_service = SimulationService()