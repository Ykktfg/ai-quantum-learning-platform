from engine.algorithms import superposition
from engine.simulator import QuantumSimulator

qc = superposition()
sim = QuantumSimulator()

print("=== Superposition ===")
print(qc.draw())
print(sim.run(qc, shots=1000))
print("Statevector:", sim.statevector(qc))
