from pathlib import Path
import importlib.util
from google import genai
from .config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def _load_local_knowledge():
    path = (
        Path(__file__).resolve().parents[3]
        / "ai"
        / "knowledge"
        / "quantum_basics.py"
    )

    spec = importlib.util.spec_from_file_location("quantum_basics", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.QUANTUM_KNOWLEDGE


def _local_fallback(prompt: str) -> str:
    knowledge = _load_local_knowledge()

    text = prompt.lower()

    priority = [
        ("hadamard", "hadamard"),
        ("cnot", "cnot"),
        ("bell", "bell_state"),
        ("entangle", "bell_state"),
        ("qubit", "qubit"),
    ]

    chosen_topic = None

    for word, topic in priority:
        if word in text:
            chosen_topic = topic
            break

    if chosen_topic:
        for item in knowledge:
            if item["topic"] == chosen_topic:
                return (
                    f"## {item['title']}\n\n"
                    f"{item['content'].strip()}"
                )

    return "Ask about qubits, Hadamard gates, CNOT gates, or Bell states."


def ask_llm(prompt: str) -> str:
    try:
        response = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
            store=False
        )
        return response.output_text

    except Exception:
        return _local_fallback(prompt)
