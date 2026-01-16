"""Cross-encoder reranking for improved retrieval precision.

Uses sentence-transformers CrossEncoder for local inference.
The model is loaded lazily on first use and cached.
"""

import logging
from typing import TYPE_CHECKING

from langchain_core.documents import Document

if TYPE_CHECKING:
    from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)

# Global cache for reranker model
_reranker_instance: "CrossEncoder | None" = None
_reranker_model_name: str | None = None


def get_reranker(model_name: str = "BAAI/bge-reranker-v2-m3") -> "CrossEncoder":
    """Get or create cached reranker instance.

    Args:
        model_name: HuggingFace model name for cross-encoder

    Returns:
        CrossEncoder instance
    """
    global _reranker_instance, _reranker_model_name

    if _reranker_instance is None or _reranker_model_name != model_name:
        # Import here to avoid loading sentence-transformers if reranking disabled
        from sentence_transformers import CrossEncoder

        logger.info(f"Loading reranker model: {model_name}")
        _reranker_instance = CrossEncoder(model_name)
        _reranker_model_name = model_name
        logger.info("Reranker model loaded successfully")

    return _reranker_instance


def rerank_documents(
    query: str,
    documents: list[Document],
    top_n: int = 5,
    model_name: str = "BAAI/bge-reranker-v2-m3",
) -> list[Document]:
    """Rerank documents using cross-encoder model.

    Cross-encoders process (query, document) pairs together,
    allowing for deeper semantic matching than bi-encoders.

    Args:
        query: Search query
        documents: Retrieved documents to rerank
        top_n: Number of top documents to return
        model_name: HuggingFace model name

    Returns:
        Top-n documents sorted by reranking score, with score in metadata
    """
    if not documents:
        return []

    if len(documents) <= top_n:
        # No need to rerank if we have fewer docs than requested
        logger.debug(f"Skipping rerank: only {len(documents)} docs (top_n={top_n})")
        return documents

    model = get_reranker(model_name)

    # Create query-document pairs for cross-encoder
    pairs = [(query, doc.page_content) for doc in documents]

    # Get reranking scores
    logger.debug(f"Reranking {len(pairs)} documents")
    scores = model.predict(pairs)

    # Pair documents with scores and sort
    scored_docs = list(zip(documents, scores))
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    # Return top_n with rerank score in metadata
    result = []
    for doc, score in scored_docs[:top_n]:
        # Create new document to avoid mutating original
        reranked_doc = Document(
            page_content=doc.page_content,
            metadata={**doc.metadata, "rerank_score": float(score)},
        )
        result.append(reranked_doc)

    logger.debug(f"Reranking complete. Top score: {scores[0]:.4f}")
    return result
