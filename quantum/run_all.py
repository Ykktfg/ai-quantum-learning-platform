from engine.algorithms import superposition, bell_state, ghz_state
from engine.simulator import QuantumSimulator

sim = QuantumSimulator()

demos = [
    ("Superposition", superposition()),
    ("Bell State", bell_state()),
    ("GHZ State", ghz_state()),
]

for name, circuit in demos:
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)
    print(circuit.draw())
    print(sim.run(circuit, shots=1000))
    print("Statevector:", sim.statevector(circuit))
