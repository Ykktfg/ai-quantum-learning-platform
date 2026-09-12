def build_quantum_context(
    simulation_result: dict | None = None,
    module: str | None = None,
    student_level: str | None = None,
) -> dict:
    """
    Build a clean, verified context object for the AI tutor.

    Simulation results should come from the quantum simulator.
    """

    context = {}

    if module:
        context["module"] = module

    if student_level:
        context["student_level"] = student_level

    if simulation_result:
        context["simulation"] = {
            "algorithm": simulation_result.get("algorithm"),
            "shots": simulation_result.get("shots"),
            "counts": simulation_result.get("counts"),
            "num_qubits": simulation_result.get("num_qubits"),
            "depth": simulation_result.get("depth"),
            "size": simulation_result.get("size"),
        }

    return context
