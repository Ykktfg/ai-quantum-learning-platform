from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile

# Educational teleportation example.
# Message qubit starts in |1>. Qubits 1 and 2 form the entangled pair.
qc = QuantumCircuit(3, 3)
qc.x(0)

qc.h(1)
qc.cx(1, 2)

qc.cx(0, 1)
qc.h(0)

qc.measure(0, 0)
qc.measure(1, 1)

# Qiskit 2.x control-flow correction.
with qc.if_test((qc.clbits[1], True)):
    qc.x(2)
with qc.if_test((qc.clbits[0], True)):
    qc.z(2)

qc.measure(2, 2)

simulator = AerSimulator()
compiled = transpile(qc, simulator)
result = simulator.run(compiled, shots=1000).result()

print("=== Quantum Teleportation ===")
print(qc.draw())
print("Counts:", result.get_counts())
print("Expected: Bob's final bit (rightmost classical bit in the displayed count) is usually 1.")
