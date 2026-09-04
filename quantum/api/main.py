from fastapi import FastAPI
from pydantic import BaseModel, Field

from engine.algorithms import superposition, bell_state, ghz_state
from engine.simulator import QuantumSimulator
from engine.circuit_builder import build_circuit
from engine.circuit_analyzer import analyze_circuit
from engine.state_analyzer import analyze_statevector
from engine.measurement_analyzer import analyze_measurements


app = FastAPI(
    title="AI Quantum Learning Platform API",
    description="Quantum circuit simulation and educational analysis API",
    version="1.0.0",
)

simulator = QuantumSimulator()


class Gate(BaseModel):
    gate: str
    qubit: int | None = None
    control: int | None = None
    target: int | None = None
    control1: int | None = None
    control2: int | None = None
    angle: float | None = None


class SimulationRequest(BaseModel):
    algorithm: str | None = None
    qubits: int | None = Field(default=None, ge=1)
    gates: list[Gate] | None = None
    shots: int = Field(default=1000, ge=1)


@app.get("/")
def home():
    return {
        "message": "Quantum API is running",
        "service": "AI Quantum Learning Platform",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/simulate")
def simulate(request: SimulationRequest):

    # --------------------------------
    # PRE-BUILT ALGORITHMS
    # --------------------------------

    if request.algorithm:

        algorithms = {
            "superposition": superposition,
            "bell": bell_state,
            "ghz": ghz_state,
        }

        algorithm_name = request.algorithm.lower()

        if algorithm_name not in algorithms:
            return {
                "error": "Unknown algorithm",
                "available_algorithms": list(algorithms.keys()),
            }

        circuit = algorithms[algorithm_name]()

        result = simulator.run(
            circuit,
            shots=request.shots,
        )

        statevector = simulator.statevector(circuit)

        circuit_analysis = analyze_circuit(circuit)

        state_analysis = analyze_statevector(
            statevector,
            circuit.num_qubits,
        )

        measurement_analysis = analyze_measurements(
            result["counts"],
            result["shots"],
        )

        return {
            "algorithm": algorithm_name,

            "simulation": {
                "counts": result["counts"],
                "probabilities": result["probabilities"],
                "shots": result["shots"],
            },

            "circuit": {
                "num_qubits": result["num_qubits"],
                "depth": result["depth"],
                "size": result["size"],
                "total_gates": circuit_analysis["total_gates"],
                "gate_counts": circuit_analysis["gate_counts"],
            },

            "state": {
                "statevector": statevector,
                "nonzero_states": state_analysis["nonzero_states"],
                "probabilities": state_analysis["probabilities"],
                "total_probability": state_analysis["total_probability"],
                "is_normalized": state_analysis["is_normalized"],
                "state_expression": state_analysis["state_expression"],
            },

            "measurement": {
                "most_likely_state": measurement_analysis[
                    "most_likely_state"
                ],
                "most_likely_probability": measurement_analysis[
                    "most_likely_probability"
                ],
                "entropy": measurement_analysis["entropy"],
                "distribution": measurement_analysis["distribution"],
                "interpretation": measurement_analysis["interpretation"],
            },

            "education": {
                "has_superposition": circuit_analysis[
                    "has_superposition"
                ],
                "has_entanglement": circuit_analysis[
                    "has_entanglement"
                ],
                "explanation": circuit_analysis["explanation"],
            },

            "circuit_diagram": str(circuit.draw()),
        }

    # --------------------------------
    # CUSTOM CIRCUIT
    # --------------------------------

    if request.qubits is None:
        return {
            "error": "qubits is required for a custom circuit"
        }

    if request.gates is None:
        return {
            "error": "gates is required for a custom circuit"
        }

    try:

        gates = [
            gate.model_dump(exclude_none=True)
            for gate in request.gates
        ]

        circuit = build_circuit(
            num_qubits=request.qubits,
            gates=gates,
        )

        result = simulator.run(
            circuit,
            shots=request.shots,
        )

        statevector = simulator.statevector(circuit)

        circuit_analysis = analyze_circuit(circuit)

        state_analysis = analyze_statevector(
            statevector,
            circuit.num_qubits,
        )

        measurement_analysis = analyze_measurements(
            result["counts"],
            result["shots"],
        )

        return {
            "algorithm": "custom",

            "simulation": {
                "counts": result["counts"],
                "probabilities": result["probabilities"],
                "shots": result["shots"],
            },

            "circuit": {
                "num_qubits": result["num_qubits"],
                "depth": result["depth"],
                "size": result["size"],
                "total_gates": circuit_analysis["total_gates"],
                "gate_counts": circuit_analysis["gate_counts"],
            },

            "state": {
                "statevector": statevector,
                "nonzero_states": state_analysis["nonzero_states"],
                "probabilities": state_analysis["probabilities"],
                "total_probability": state_analysis["total_probability"],
                "is_normalized": state_analysis["is_normalized"],
                "state_expression": state_analysis["state_expression"],
            },

            "measurement": {
                "most_likely_state": measurement_analysis[
                    "most_likely_state"
                ],
                "most_likely_probability": measurement_analysis[
                    "most_likely_probability"
                ],
                "entropy": measurement_analysis["entropy"],
                "distribution": measurement_analysis["distribution"],
                "interpretation": measurement_analysis["interpretation"],
            },

            "education": {
                "has_superposition": circuit_analysis[
                    "has_superposition"
                ],
                "has_entanglement": circuit_analysis[
                    "has_entanglement"
                ],
                "explanation": circuit_analysis["explanation"],
            },

            "circuit_diagram": str(circuit.draw()),
        }

    except (KeyError, ValueError, TypeError) as exc:
        return {
            "error": str(exc)
        }