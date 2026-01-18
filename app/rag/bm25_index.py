"""BM25 sparse retrieval for hybrid search."""

import re

from rank_bm25 import BM25Okapi


class BM25Index:
    """BM25 index for keyword-based retrieval.

    Used alongside dense vector search to improve retrieval of
    documents containing specific terms like proper nouns, product names,
    and technical terminology that embedding models may struggle with.
    """

    def __init__(self) -> None:
        """Initialize empty BM25 index."""
        self.index: BM25Okapi | None = None
        self.doc_ids: list[str] = []
        self.doc_contents: dict[str, str] = {}  # id -> content mapping

    def tokenize(self, text: str) -> list[str]:
        """Tokenize text for BM25.

        Args:
            text: Text to tokenize.

        Returns:
            List of lowercase word tokens.
        """
        text = text.lower()
        tokens = re.findall(r"\b\w+\b", text)
        return tokens

    def build_index(self, documents: list[dict]) -> None:
        """Build BM25 index from documents.

        Args:
            documents: List of dicts with 'id' and 'content' keys.
        """
        self.doc_ids = [doc["id"] for doc in documents]
        self.doc_contents = {doc["id"]: doc["content"] for doc in documents}

        corpus = [self.tokenize(doc["content"]) for doc in documents]
        self.index = BM25Okapi(corpus)

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        """Search index and return doc IDs with BM25 scores.

        Args:
            query: Search query.
            top_k: Number of results to return.

        Returns:
            List of (doc_id, score) tuples sorted by score descending.
        """
        if self.index is None:
            return []

        tokens = self.tokenize(query)
        scores = self.index.get_scores(tokens)

        # Pair with doc IDs and sort by score
        results = list(zip(self.doc_ids, scores))
        results.sort(key=lambda x: x[1], reverse=True)

        return [(doc_id, float(score)) for doc_id, score in results[:top_k]]

    def get_content(self, doc_id: str) -> str | None:
        """Get document content by ID.

        Args:
            doc_id: Document ID.

        Returns:
            Document content or None if not found.
        """
        return self.doc_contents.get(doc_id)


# Global singleton for the BM25 index
_bm25_index: BM25Index | None = None


def get_bm25_index() -> BM25Index:
    """Get the global BM25 index instance.

    Returns:
        BM25Index instance.
    """
    global _bm25_index
    if _bm25_index is None:
        _bm25_index = BM25Index()
    return _bm25_index


def reset_bm25_index() -> None:
    """Reset the global BM25 index (for re-indexing)."""
    global _bm25_index
    _bm25_index = None
