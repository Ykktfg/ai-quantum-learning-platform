from engine.algorithms import superposition, bell_state
from engine.simulator import QuantumSimulator


def test_superposition_has_two_outcomes():
    result = QuantumSimulator().run(superposition(), shots=1000)
    assert set(result["counts"]).issubset({"0", "1"})
    assert sum(result["counts"].values()) == 1000


def test_bell_state_has_only_correlated_outcomes():
    result = QuantumSimulator().run(bell_state(), shots=1000)
    assert set(result["counts"]).issubset({"00", "11"})
    assert sum(result["counts"].values()) == 1000
