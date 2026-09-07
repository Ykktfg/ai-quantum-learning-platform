from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def deutsch_oracle(oracle_type: str) -> QuantumCircuit:
    """Build one of Deutsch's two representative oracles.

    constant: f(x)=0
    balanced: f(x)=x
    """
    qc = QuantumCircuit(2)

    if oracle_type == "constant":
        pass
    elif oracle_type == "balanced":
        qc.cx(0, 1)
    else:
        raise ValueError("oracle_type must be 'constant' or 'balanced'")

    return qc


def deutsch(oracle_type: str) -> QuantumCircuit:
    qc = QuantumCircuit(2, 1)

    # |0>|1>
    qc.x(1)

    # H both qubits
    qc.h(0)
    qc.h(1)

    qc.compose(deutsch_oracle(oracle_type), inplace=True)

    # Interference
    qc.h(0)
    qc.measure(0, 0)

    return qc


simulator = AerSimulator()

for oracle_type in ("constant", "balanced"):
    qc = deutsch(oracle_type)
    result = simulator.run(transpile(qc, simulator), shots=1000).result()
    counts = result.get_counts()

    print(f"=== Deutsch Algorithm: {oracle_type} oracle ===")
    print(qc.draw())
    print("Counts:", counts)
    print("Interpretation: 0 -> constant, 1 -> balanced")
    print()
