from typing import List
import math

from ai.rag.embeddings import create_embeddings
from ai.rag.vector_store import load_vector_store


def cosine_similarity(
    vector_a: List[float],
    vector_b: List[float],
) -> float:
    """
    Calculate cosine similarity between two vectors.
    """
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )


def retrieve(
    question: str,
    top_k: int = 3,
) -> List[dict]:
    """
    Retrieve the most semantically relevant
    quantum knowledge chunks for a question.

    Knowledge-base embeddings are loaded from
    the local vector store. Only the student's
    question is embedded at query time.
    """

    vector_store = load_vector_store()

    if not vector_store:
        return []

    question_embedding = create_embeddings(
        [question]
    )[0]

    scored_chunks = []

    for chunk in vector_store:
        similarity = cosine_similarity(
            question_embedding,
            chunk["embedding"],
        )

        scored_chunks.append(
            {
                "topic": chunk["topic"],
                "title": chunk["title"],
                "content": chunk["content"],
                "score": similarity,
            }
        )

    scored_chunks.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return scored_chunks[:top_k]
