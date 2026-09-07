from engine.algorithms import ghz_state
from engine.simulator import QuantumSimulator

qc = ghz_state()
sim = QuantumSimulator()

print("=== 3-Qubit GHZ State ===")
print(qc.draw())
print(sim.run(qc, shots=1000))
print("Statevector:", sim.statevector(qc))
