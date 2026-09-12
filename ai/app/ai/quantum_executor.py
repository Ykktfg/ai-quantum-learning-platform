import ast

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


MAX_QUBITS = 20
MAX_SHOTS = 10000


FORBIDDEN_NAMES = {
    "eval",
    "exec",
    "open",
    "compile",
    "input",
    "__import__",
    "globals",
    "locals",
    "vars",
    "getattr",
    "setattr",
    "delattr",
}


FORBIDDEN_ATTRIBUTES = {
    "__class__",
    "__bases__",
    "__subclasses__",
    "__globals__",
    "__builtins__",
    "__dict__",
    "__code__",
}


def validate_execution_safety(code: str) -> dict:
    """
    Perform deterministic safety checks before executing
    AI-generated quantum code.
    """

    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return {
            "safe": False,
            "stage": "syntax",
            "error": (
                f"Syntax error on line {error.lineno}: "
                f"{error.msg}"
            ),
        }

    for node in ast.walk(tree):

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return {
                "safe": False,
                "stage": "security",
                "error": (
                    "Import statements are not allowed "
                    "during quantum code execution."
                ),
            }

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in FORBIDDEN_NAMES:
                    return {
                        "safe": False,
                        "stage": "security",
                        "error": (
                            f"Forbidden function '{node.func.id}' "
                            "was found."
                        ),
                    }

        if isinstance(node, ast.Name):
            if node.id in FORBIDDEN_NAMES:
                return {
                    "safe": False,
                    "stage": "security",
                    "error": (
                        f"Forbidden name '{node.id}' "
                        "was found."
                    ),
                }

        if isinstance(node, ast.Attribute):
            if node.attr in FORBIDDEN_ATTRIBUTES:
                return {
                    "safe": False,
                    "stage": "security",
                    "error": (
                        f"Forbidden attribute '{node.attr}' "
                        "was found."
                    ),
                }

    return {
        "safe": True,
        "stage": "security",
        "error": None,
    }


def execute_quantum_code(code: str) -> dict:
    """
    Execute basic Qiskit QuantumCircuit code
    after deterministic safety validation.
    """

    safety_result = validate_execution_safety(code)

    if not safety_result["safe"]:
        return {
            "success": False,
            "stage": safety_result["stage"],
            "error": safety_result["error"],
        }

    try:
        namespace = {
            "QuantumCircuit": QuantumCircuit,
        }

        exec(
            code,
            {"__builtins__": {}},
            namespace,
        )

    except Exception as error:
        return {
            "success": False,
            "stage": "execution",
            "error": str(error),
        }

    circuits = [
        value
        for value in namespace.values()
        if isinstance(value, QuantumCircuit)
    ]

    if not circuits:
        return {
            "success": False,
            "stage": "execution",
            "error": "No QuantumCircuit object was created.",
        }

    circuit = circuits[0]

    if circuit.num_qubits > MAX_QUBITS:
        return {
            "success": False,
            "stage": "limits",
            "error": (
                f"Circuit has {circuit.num_qubits} qubits. "
                f"Maximum allowed is {MAX_QUBITS}."
            ),
        }

    return {
        "success": True,
        "stage": "execution",
        "error": None,
        "num_qubits": circuit.num_qubits,
        "depth": circuit.depth(),
        "size": circuit.size(),
        "operations": dict(circuit.count_ops()),
    }


def simulate_quantum_code(
    code: str,
    shots: int = 1024,
) -> dict:
    """
    Execute a Qiskit circuit and run it
    on the local Qiskit Aer simulator.
    """

    safety_result = validate_execution_safety(code)

    if not safety_result["safe"]:
        return {
            "success": False,
            "stage": safety_result["stage"],
            "error": safety_result["error"],
        }

    if shots <= 0:
        return {
            "success": False,
            "stage": "limits",
            "error": "Shots must be greater than zero.",
        }

    if shots > MAX_SHOTS:
        return {
            "success": False,
            "stage": "limits",
            "error": (
                f"Shots cannot exceed {MAX_SHOTS}."
            ),
        }

    try:
        namespace = {
            "QuantumCircuit": QuantumCircuit,
        }

        exec(
            code,
            {"__builtins__": {}},
            namespace,
        )

    except Exception as error:
        return {
            "success": False,
            "stage": "execution",
            "error": str(error),
        }

    circuits = [
        value
        for value in namespace.values()
        if isinstance(value, QuantumCircuit)
    ]

    if not circuits:
        return {
            "success": False,
            "stage": "execution",
            "error": "No QuantumCircuit object was created.",
        }

    circuit = circuits[0]

    if circuit.num_qubits > MAX_QUBITS:
        return {
            "success": False,
            "stage": "limits",
            "error": (
                f"Circuit has {circuit.num_qubits} qubits. "
                f"Maximum allowed is {MAX_QUBITS}."
            ),
        }

    try:
        simulation_circuit = circuit.copy()

        if simulation_circuit.num_clbits == 0:
            simulation_circuit.measure_all()

        simulator = AerSimulator()

        result = simulator.run(
            simulation_circuit,
            shots=shots,
        ).result()

        counts = result.get_counts()

        return {
            "success": True,
            "stage": "simulation",
            "error": None,
            "num_qubits": circuit.num_qubits,
            "depth": circuit.depth(),
            "size": circuit.size(),
            "operations": dict(circuit.count_ops()),
            "shots": shots,
            "counts": dict(counts),
        }

    except Exception as error:
        return {
            "success": False,
            "stage": "simulation",
            "error": str(error),
        }
