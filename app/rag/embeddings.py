"""Embedding utilities for RAG pipeline."""

from app.llm import get_embeddings


def embed_text(text: str) -> list[float]:
    """Embed a single text string into a vector.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    embeddings = get_embeddings()
    return embeddings.embed_query(text)


def embed_documents(texts: list[str]) -> list[list[float]]:
    """Embed multiple texts into vectors.

    Args:
        texts: A list of texts to embed.

    Returns:
        A list of embedding vectors, one per input text.
    """
    embeddings = get_embeddings()
    return embeddings.embed_documents(texts)
