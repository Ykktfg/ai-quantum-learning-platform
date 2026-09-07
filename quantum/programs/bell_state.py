from engine.algorithms import bell_state
from engine.simulator import QuantumSimulator

qc = bell_state()
sim = QuantumSimulator()

print("=== Bell State / Entanglement ===")
print(qc.draw())
print(sim.run(qc, shots=1000))
print("Statevector:", sim.statevector(qc))
