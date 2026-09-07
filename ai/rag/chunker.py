from ai.knowledge.quantum_basics import QUANTUM_KNOWLEDGE


def chunk_knowledge(
    knowledge: list[dict],
    max_chars: int = 800,
) -> list[dict]:
    """
    Convert structured knowledge entries into smaller searchable chunks.

    Each chunk keeps the original topic and title so the retriever
    can identify where the information came from.
    """

    chunks = []

    for entry in knowledge:

        topic = entry.get("topic", "")
        title = entry.get("title", "")
        content = entry.get("content", "").strip()

        if not content:
            continue

        paragraphs = [
            paragraph.strip()
            for paragraph in content.split("\n\n")
            if paragraph.strip()
        ]

        current_chunk = ""

        for paragraph in paragraphs:

            if len(current_chunk) + len(paragraph) + 2 <= max_chars:
                if current_chunk:
                    current_chunk += "\n\n"

                current_chunk += paragraph

            else:

                if current_chunk:
                    chunks.append(
                        {
                            "topic": topic,
                            "title": title,
                            "content": current_chunk,
                        }
                    )

                current_chunk = paragraph

        if current_chunk:
            chunks.append(
                {
                    "topic": topic,
                    "title": title,
                    "content": current_chunk,
                }
            )

    return chunks


def build_knowledge_chunks() -> list[dict]:
    """
    Build searchable chunks from the quantum knowledge base.
    """

    return chunk_knowledge(QUANTUM_KNOWLEDGE)
