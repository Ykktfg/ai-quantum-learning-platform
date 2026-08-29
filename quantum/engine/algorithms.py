from qiskit import QuantumCircuit


def superposition() -> QuantumCircuit:
    """One qubit in |+>."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def bell_state() -> QuantumCircuit:
    """Create the Bell state (|00> + |11>) / sqrt(2)."""
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


def ghz_state() -> QuantumCircuit:
    """Create the 3-qubit GHZ state."""
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc


def teleportation() -> QuantumCircuit:
    """Standard 3-qubit quantum teleportation circuit.

    The input state is |1>, so the receiver should recover |1>
    after classical correction.
    """
    qc = QuantumCircuit(3, 2)

    # Prepare the message qubit in |1>.
    qc.x(0)

    # Create entanglement between qubits 1 and 2.
    qc.h(1)
    qc.cx(1, 2)

    # Bell measurement of message qubit and Alice's entangled qubit.
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, 0)
    qc.measure(1, 1)

    # Bob's corrections, controlled by Alice's classical results.
    with qc.if_test((qc.clbits[1], True)) as else_:
        qc.x(2)
    with qc.if_test((qc.clbits[0], True)):
        qc.z(2)

    # Add a final classical bit to record Bob's result.
    # The original circuit has only two classical bits, so create a
    # separate measurement circuit for the final result in the demo.
    return qc
