import ast


def validate_python_syntax(code: str) -> dict:
    """
    Validate Python syntax without executing the code.
    """

    try:
        ast.parse(code)

        return {
            "valid": True,
            "error": None,
        }

    except SyntaxError as error:
        return {
            "valid": False,
            "error": (
                f"Syntax error on line {error.lineno}: "
                f"{error.msg}"
            ),
        }


def validate_quantum_code(code: str) -> dict:
    """
    Perform deterministic validation of quantum code.

    Checks:
    1. Python syntax
    2. Presence of a Qiskit quantum circuit
    """

    syntax_result = validate_python_syntax(code)

    if not syntax_result["valid"]:
        return {
            "valid": False,
            "stage": "syntax",
            "error": syntax_result["error"],
        }

    try:
        tree = ast.parse(code)

    except SyntaxError as error:
        return {
            "valid": False,
            "stage": "syntax",
            "error": str(error),
        }

    has_quantum_circuit = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id == "QuantumCircuit":
                    has_quantum_circuit = True

            elif isinstance(node.func, ast.Attribute):
                if node.func.attr == "QuantumCircuit":
                    has_quantum_circuit = True

    if not has_quantum_circuit:
        return {
            "valid": False,
            "stage": "quantum",
            "error": (
                "No Qiskit QuantumCircuit was found "
                "in the provided code."
            ),
        }

    return {
        "valid": True,
        "stage": "quantum",
        "error": None,
    }
