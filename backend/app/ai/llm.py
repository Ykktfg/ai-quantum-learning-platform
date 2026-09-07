from pathlib import Path
import importlib.util

from google import genai

from .config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


def _load_local_knowledge():
    knowledge_path = (
        Path(__file__).resolve().parents[3]
        / "ai"
        / "knowledge"
        / "quantum_basics.py"
    )

    if not knowledge_path.exists():
        return []

    spec = importlib.util.spec_from_file_location(
        "quantum_basics",
        knowledge_path
    )

    if spec is None or spec.loader is None:
        return []

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(module, "QUANTUM_KNOWLEDGE", [])


def _local_fallback(prompt: str) -> str:
    knowledge = _load_local_knowledge()
    text = prompt.lower()

    if not knowledge:
        return (
            "## Quantum AI Tutor\n\n"
            "The local Quantum Knowledge Base is currently unavailable."
        )

    best_match = None
    best_score = 0

    keyword_map = {
        "hadamard": ["hadamard", " h gate", " h-gate"],
        "qubit": ["qubit", "quantum bit"],
        "superposition": ["superposition"],
        "measurement": ["measurement", "measure", "measuring"],
        "pauli_x": ["pauli x", "pauli-x", " x gate"],
        "pauli_y": ["pauli y", "pauli-y", " y gate"],
        "pauli_z": ["pauli z", "pauli-z", " z gate"],
        "cnot": ["cnot", "controlled not", "cx gate"],
        "entanglement": ["entanglement", "entangled"],
        "bell_state": ["bell state", "bell-state"],
        "ghz_state": ["ghz", "ghz state"],
        "quantum_circuit": ["quantum circuit", "circuit"],
    }

    for item in knowledge:
        topic = item.get("topic", "").lower()
        title = item.get("title", "").lower()

        score = 0

        if topic in text:
            score += 10

        if title and title in text:
            score += 8

        for key, keywords in keyword_map.items():
            if key in topic:
                for keyword in keywords:
                    if keyword.strip() in text:
                        score += 10

        topic_words = topic.replace("_", " ").split()

        for word in topic_words:
            if len(word) > 2 and word in text:
                score += 2

        if score > best_score:
            best_score = score
            best_match = item

    if best_match:
        return best_match["content"].strip()

    return (
        "## Quantum AI Tutor\n\n"
        "I can answer questions about:\n\n"
        "- Qubits\n"
        "- Superposition\n"
        "- Measurement\n"
        "- Hadamard gates\n"
        "- Pauli gates\n"
        "- CNOT gates\n"
        "- Entanglement\n"
        "- Bell states\n"
        "- GHZ states\n"
        "- Quantum circuits"
    )


def ask_llm(prompt: str) -> str:
    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
            store=False
        )

        return interaction.output_text

    except Exception:
        return _local_fallback(prompt)
