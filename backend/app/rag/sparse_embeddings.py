"""
Sparse embeddings for BM25 hybrid search.

Uses FastEmbed's BM25 implementation optimized for Qdrant.
"""

from dataclasses import dataclass

from langfuse import observe

from backend.app.core.config import settings


@dataclass
class SparseVector:
    """Sparse vector representation for BM25."""

    indices: list[int]
    values: list[float]

    def to_qdrant(self):
        """Convert to Qdrant sparse vector format."""
        from qdrant_client.http import models as qdrant_models

        return qdrant_models.SparseVector(
            indices=self.indices,
            values=self.values,
        )


class BM25Embeddings:
    """
    BM25 sparse embeddings using FastEmbed.

    Generates sparse vectors compatible with Qdrant's sparse vector search.
    Uses the Qdrant/bm25 model from FastEmbed for efficient tokenization.
    """

    def __init__(self, model_name: str | None = None):
        """
        Initialize BM25 embeddings.

        Args:
            model_name: Model identifier (defaults to settings.bm25_model)
        """
        self.model_name = model_name or settings.bm25_model
        self._model = None

    def _get_model(self):
        """Lazy-load the BM25 model."""
        if self._model is None:
            from fastembed import SparseTextEmbedding

            self._model = SparseTextEmbedding(model_name=self.model_name)
        return self._model

    @observe(name="bm25_embed_documents")
    def embed_documents(self, texts: list[str]) -> list[SparseVector]:
        """
        Generate sparse embeddings for documents.

        Args:
            texts: List of document texts

        Returns:
            List of SparseVector objects
        """
        model = self._get_model()
        embeddings = list(model.embed(texts))

        return [
            SparseVector(
                indices=emb.indices.tolist(),
                values=emb.values.tolist(),
            )
            for emb in embeddings
        ]

    @observe(name="bm25_embed_query")
    def embed_query(self, text: str) -> SparseVector:
        """
        Generate sparse embedding for a query.

        Args:
            text: Query text

        Returns:
            SparseVector object
        """
        model = self._get_model()
        # query_embed returns a generator, get first result
        embeddings = list(model.query_embed(text))
        emb = embeddings[0]

        return SparseVector(
            indices=emb.indices.tolist(),
            values=emb.values.tolist(),
        )


# Singleton instance for reuse
_bm25_embeddings: BM25Embeddings | None = None


def get_bm25_embeddings() -> BM25Embeddings:
    """Get or create BM25 embeddings instance."""
    global _bm25_embeddings
    if _bm25_embeddings is None:
        _bm25_embeddings = BM25Embeddings()
    return _bm25_embeddings
