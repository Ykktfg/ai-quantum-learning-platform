from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from engine.algorithms import superposition, bell_state, ghz_state
from engine.circuit_builder import build_circuit
from engine.simulator import QuantumSimulator


app = FastAPI(
    title="AI Quantum Learning Platform API",
    description="Quantum circuit simulation API",
    version="1.0.0",
)

simulator = QuantumSimulator()


class Gate(BaseModel):
    gate: str
    qubit: int | None = None
    control: int | None = None
    target: int | None = None
    angle: float | None = None
    qubit1: int | None = None
    qubit2: int | None = None


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

        return {
            "algorithm": algorithm_name,
            "counts": result["counts"],
            "shots": result["shots"],
            "num_qubits": result["num_qubits"],
            "depth": result["depth"],
            "size": result["size"],
            "statevector": simulator.statevector(circuit),
            "circuit": str(circuit.draw()),
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

        return {
            "algorithm": "custom",
            "counts": result["counts"],
            "shots": result["shots"],
            "num_qubits": result["num_qubits"],
            "depth": result["depth"],
            "size": result["size"],
            "statevector": simulator.statevector(circuit),
            "circuit": str(circuit.draw()),
        }

    except (KeyError, ValueError, TypeError) as exc:
        return {
            "error": str(exc)
        }