from fastapi import FastAPI
from pydantic import BaseModel

from engine.algorithms import superposition, bell_state, ghz_state
from engine.simulator import QuantumSimulator


app = FastAPI(
    title="AI Quantum Learning Platform API",
    description="Quantum circuit simulation API",
    version="1.0.0",
)

simulator = QuantumSimulator()


class SimulationRequest(BaseModel):
    algorithm: str
    shots: int = 1000


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

    algorithms = {
        "superposition": superposition,
        "bell": bell_state,
        "ghz": ghz_state,
    }

    if request.algorithm not in algorithms:
        return {
            "error": "Unknown algorithm",
            "available_algorithms": list(algorithms.keys()),
        }

    circuit = algorithms[request.algorithm]()

    result = simulator.run(
        circuit,
        shots=request.shots
    )

    return {
        "algorithm": request.algorithm,
        "counts": result["counts"],
        "shots": result["shots"],
        "num_qubits": result["num_qubits"],
        "depth": result["depth"],
        "size": result["size"],
        "statevector": simulator.statevector(circuit),
        "circuit": str(circuit.draw()),
    }