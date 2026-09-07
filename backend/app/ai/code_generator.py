import re

from .llm import ask_llm
from .prompts import SYSTEM_PROMPT
from .code_validator import validate_quantum_code


CODE_GENERATION_PROMPT = """
You are the quantum code generation assistant for an
interactive quantum computing learning platform.

Generate Qiskit Python code from the student's request.

Requirements:

1. Generate clear and beginner-friendly Qiskit code.
2. Use QuantumCircuit for circuit construction.
3. Keep the generated circuit as simple as possible.
4. Explain what the generated circuit does.
5. Do not invent simulation results.
6. Do not claim measurement counts or probabilities.
7. Do not execute the code.
8. Return only the requested quantum program and explanation.
9. Prefer standard Qiskit circuit operations.
10. If the student's request is ambiguous, make a reasonable
    educational assumption and state it briefly.

Response format:

Explanation:

<short explanation>

Code:

<complete Qiskit code>
"""


def extract_code_from_response(response: str) -> str:
    """
    Extract Python code from an LLM response.
    """

    match = re.search(
        r"```python\s*(.*?)```",
        response,
        re.DOTALL | re.IGNORECASE,
    )

    if match:
        return match.group(1).strip()

    match = re.search(
        r"```\s*(.*?)```",
        response,
        re.DOTALL,
    )

    if match:
        return match.group(1).strip()

    code_match = re.search(
        r"(qc\s*=\s*QuantumCircuit\(.*)",
        response,
        re.DOTALL,
    )

    if code_match:
        return code_match.group(1).strip()

    return response.strip()


def generate_quantum_code(
    request: str,
    quantum_context: dict | None = None,
) -> str:
    """
    Generate Qiskit quantum code using the LLM.

    The generated code is validated deterministically
    before being returned.
    """

    context_text = ""

    if quantum_context:
        context_text = (
            "\n\nVerified quantum context:\n"
            + str(quantum_context)
        )

    prompt = (
        SYSTEM_PROMPT
        + "\n\n"
        + CODE_GENERATION_PROMPT
        + context_text
        + "\n\n"
        + "Student request:\n"
        + request
    )

    response = ask_llm(prompt)

    if not response:
        return (
            "The AI tutor could not generate code "
            "because the language model returned no response."
        )

    quota_message = (
        "The AI tutor is temporarily unavailable because "
        "the Gemini API quota has been exceeded."
    )

    if quota_message in response:
        return response

    code = extract_code_from_response(response)

    validation_result = validate_quantum_code(code)

    if not validation_result["valid"]:
        return (
            response
            + "\n\n"
            + "Generated code validation:\n"
            + "FAILED\n"
            + "Stage: "
            + validation_result["stage"]
            + "\n"
            + "Problem: "
            + validation_result["error"]
        )

    return (
        response
        + "\n\n"
        + "Generated code validation:\n"
        + "PASSED"
    )
