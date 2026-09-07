import json
from pathlib import Path
from typing import List

from ai.rag.embeddings import embed_knowledge_base


VECTOR_STORE_PATH = (
    Path(__file__).resolve().parent
    / "vector_store.json"
)


def build_vector_store() -> List[dict]:
    """
    Generate embeddings for the knowledge base
    and save them to a local JSON vector store.
    """

    embedded_chunks = embed_knowledge_base()

    with open(
        VECTOR_STORE_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            embedded_chunks,
            file,
        )

    return embedded_chunks


def load_vector_store() -> List[dict]:
    """
    Load previously generated knowledge embeddings
    from the local vector store.
    """

    if not VECTOR_STORE_PATH.exists():
        return build_vector_store()

    with open(
        VECTOR_STORE_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)
