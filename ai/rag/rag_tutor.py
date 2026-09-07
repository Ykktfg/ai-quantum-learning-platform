from ai.rag.retriever import retrieve
from backend.app.ai.llm import ask_llm


RAG_SYSTEM_PROMPT = """
You are the knowledge-grounded AI Tutor for an interactive quantum
computing learning platform.

Answer the student's question using the provided knowledge context.

Teaching rules:

1. Explain concepts clearly and step by step.
2. Prefer the provided knowledge context when answering.
3. Do not invent facts that contradict the provided context.
4. If the provided context does not contain enough information, say that
   the available knowledge base does not contain enough information.
5. You may use general quantum computing knowledge to explain concepts,
   but clearly distinguish it from information retrieved from the
   knowledge base.
6. Never invent simulation results, measurement counts, state vectors,
   probabilities, or other exact computational results.
7. Keep the answer educational and appropriate for a student.
"""


def build_knowledge_context(question: str, top_k: int = 3) -> str:
    results = retrieve(question, top_k=top_k)

    if not results:
        return "No relevant knowledge-base entries were found."

    context_parts = []

    for result in results:
        context_parts.append(
            "Topic: "
            + result["topic"]
            + "\n"
            + "Title: "
            + result["title"]
            + "\n"
            + "Content:\n"
            + result["content"]
        )

    return "\n\n---\n\n".join(context_parts)


def answer_with_rag(question: str, top_k: int = 3) -> str:
    context = build_knowledge_context(
        question,
        top_k=top_k
    )

    prompt = (
        RAG_SYSTEM_PROMPT
        + "\n\n"
        + "Retrieved knowledge:\n\n"
        + context
        + "\n\n"
        + "Student question:\n"
        + question
        + "\n\n"
        + "Answer the student clearly using the retrieved knowledge."
    )

    return ask_llm(prompt)
