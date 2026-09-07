from typing import List

from google import genai
from google.genai import types

from backend.app.ai.config import GEMINI_API_KEY
from ai.rag.chunker import build_knowledge_chunks


EMBEDDING_MODEL = "gemini-embedding-001"

EMBEDDING_DIMENSION = 768


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def create_embeddings(
    texts: List[str],
) -> List[List[float]]:
    """
    Generate semantic embeddings for a list of texts
    using Gemini's embedding model.
    """

    if not texts:
        return []

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSION,
        ),
    )

    return [
        embedding.values
        for embedding in result.embeddings
    ]


def embed_knowledge_base() -> List[dict]:
    """
    Generate semantic embeddings for all
    quantum knowledge-base chunks.
    """

    chunks = build_knowledge_chunks()

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    vectors = create_embeddings(texts)

    embedded_chunks = []

    for chunk, vector in zip(chunks, vectors):

        embedded_chunks.append(
            {
                "topic": chunk["topic"],
                "title": chunk["title"],
                "content": chunk["content"],
                "embedding": vector,
            }
        )

    return embedded_chunks
