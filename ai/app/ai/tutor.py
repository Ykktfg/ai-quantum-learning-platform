from .llm import ask_llm
from .prompts import SYSTEM_PROMPT
from .context import build_quantum_context
from .code_validator import validate_quantum_code
from .quantum_executor import simulate_quantum_code

from ai.rag.rag_tutor import build_knowledge_context


def chat_with_tutor(
    question: str,
    quantum_context: dict | None = None,
) -> str:
    """
    Answer a student's question using RAG
    and optional verified quantum context.
    """

    knowledge_context = build_knowledge_context(
        question,
        top_k=3,
    )

    quantum_context_text = ""

    if quantum_context:
        normalized_context = build_quantum_context(
            simulation_result=quantum_context.get(
                "simulation"
            ),
            module=quantum_context.get("module"),
            student_level=quantum_context.get(
                "student_level"
            ),
        )

        quantum_context_text = (
            "\n\nVerified quantum context:\n"
            + str(normalized_context)
        )

    prompt = (
        SYSTEM_PROMPT
        + "\n\n"
        + "Retrieved knowledge:\n"
        + knowledge_context
        + quantum_context_text
        + "\n\n"
        + "Student question:\n"
        + question
        + "\n\n"
        + "Answer the student clearly and educationally."
    )

    return ask_llm(prompt)


def explain_circuit(
    circuit: str,
    quantum_context: dict | None = None,
) -> str:
    """
    Explain a quantum circuit using the AI tutor.
    """

    context_text = ""

    if quantum_context:
        normalized_context = build_quantum_context(
            simulation_result=quantum_context.get(
                "simulation"
            ),
            module=quantum_context.get("module"),
            student_level=quantum_context.get(
                "student_level"
            ),
        )

        context_text = (
            "\n\nVerified quantum context:\n"
            + str(normalized_context)
        )

    prompt = (
        SYSTEM_PROMPT
        + "\n\n"
        + "Explain the following quantum circuit "
        + "step by step.\n\n"
        + "Circuit:\n"
        + circuit
        + context_text
        + "\n\n"
        + "Explain:\n"
        + "1. What each gate does.\n"
        + "2. How the quantum state changes conceptually.\n"
        + "3. What the overall circuit is intended to achieve.\n"
        + "4. Any important quantum concepts involved.\n\n"
        + "Do not invent simulation results."
    )

    return ask_llm(prompt)


def debug_quantum_code(
    code: str,
    error: str | None = None,
    quantum_context: dict | None = None,
) -> str:
    """
    Validate, simulate, and debug quantum code.

    Deterministic validation and simulation happen
    before the LLM is called.
    """

    validation_result = validate_quantum_code(code)

    if not validation_result["valid"]:
        return (
            "Deterministic code validation failed.\n\n"
            + "Validation stage: "
            + validation_result["stage"]
            + "\n"
            + "Problem: "
            + validation_result["error"]
        )

    simulation_result = simulate_quantum_code(code)

    if not simulation_result["success"]:
        return (
            "Quantum simulation failed.\n\n"
            + "Simulation stage: "
            + simulation_result["stage"]
            + "\n"
            + "Problem: "
            + simulation_result["error"]
        )

    error_text = (
        error
        if error
        else "No error message was provided."
    )

    context_text = ""

    if quantum_context:
        normalized_context = build_quantum_context(
            simulation_result=quantum_context.get(
                "simulation"
            ),
            module=quantum_context.get("module"),
            student_level=quantum_context.get(
                "student_level"
            ),
        )

        context_text = (
            "\n\nAdditional verified quantum context:\n"
            + str(normalized_context)
        )

    prompt = (
        SYSTEM_PROMPT
        + "\n\n"
        + "Debug the following quantum computing code.\n\n"
        + "The code has passed deterministic syntax "
        + "and QuantumCircuit validation.\n\n"
        + "Code:\n"
        + code
        + "\n\n"
        + "Reported error:\n"
        + error_text
        + "\n\n"
        + "Verified Qiskit simulation result:\n"
        + str(simulation_result)
        + context_text
        + "\n\n"
        + "Analyze the code using the actual simulation result.\n\n"
        + "Explain:\n"
        + "1. What the code is trying to do.\n"
        + "2. What the simulation result shows.\n"
        + "3. What is wrong, if anything.\n"
        + "4. Why the problem occurs.\n"
        + "5. How to fix it.\n"
        + "6. Provide corrected code when needed.\n"
        + "7. Explain why the corrected code works.\n\n"
        + "Important:\n"
        + "- Do not invent errors.\n"
        + "- Do not invent simulation results.\n"
        + "- Treat the provided Qiskit simulation result as authoritative.\n"
        + "- If the code appears correct, say so.\n"
        + "- Keep the explanation educational."
    )

    return ask_llm(prompt)
