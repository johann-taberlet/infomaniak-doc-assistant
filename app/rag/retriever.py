"""Qdrant vector store retriever with hybrid search for RAG pipeline."""

import logging
import uuid

from langchain_core.documents import Document
from qdrant_client import QdrantClient, models

from app.config import settings
from app.rag.bm25_index import BM25Index, get_bm25_index, reset_bm25_index
from app.rag.embeddings import embed_documents, embed_text
from app.rag.query_expansion import expand_query

logger = logging.getLogger(__name__)

# Batch size for scrolling through Qdrant collection
_QDRANT_SCROLL_BATCH_SIZE = 100


def _create_document(payload: dict, score: float) -> Document:
    """Create a Document from Qdrant payload.

    Args:
        payload: Qdrant point payload with content and metadata.
        score: Relevance score (RRF or vector similarity).

    Returns:
        Document with page_content and metadata.
    """
    return Document(
        page_content=payload.get("content", ""),
        metadata={
            "source": payload.get("source", ""),
            "title": payload.get("title", ""),
            "product": payload.get("product", ""),
            "score": score,
        },
    )


class QdrantRetriever:
    """Retriever class for Qdrant with hybrid search (vector + BM25)."""

    def __init__(self) -> None:
        """Initialize the Qdrant client connection."""
        self.client = QdrantClient(
            url=settings.QDRANT_HOST,
            api_key=settings.QDRANT_API_KEY or None,
        )
        self.collection_name = settings.QDRANT_COLLECTION
        self._bm25_initialized = False

    def create_collection(self, force_recreate: bool = False) -> None:
        """Create the collection if it doesn't exist.

        Args:
            force_recreate: If True, delete existing collection and recreate.
        """
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]

        if force_recreate and self.collection_name in collection_names:
            self.client.delete_collection(self.collection_name)
            collection_names.remove(self.collection_name)
            # Reset BM25 index when collection is recreated
            reset_bm25_index()
            self._bm25_initialized = False

        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=settings.RAG_VECTOR_DIMENSION,
                    distance=models.Distance.COSINE,
                ),
            )

    def upsert(self, chunks: list[Document], batch_size: int = 50) -> int:
        """Upsert document chunks into the collection in batches.

        Args:
            chunks: List of Document objects with page_content and metadata.
            batch_size: Number of chunks to upsert per batch (default: 50).

        Returns:
            Number of points upserted.
        """
        if not chunks:
            return 0

        total_upserted = 0

        # Process in batches to avoid payload size limits
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]

            # Extract texts and embed them
            texts = [chunk.page_content for chunk in batch]
            vectors = embed_documents(texts)

            # Build points with unique IDs
            points = []
            for chunk, vector in zip(batch, vectors):
                point = models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "content": chunk.page_content,
                        "source": chunk.metadata.get("source", ""),
                        "title": chunk.metadata.get("title", ""),
                        "product": chunk.metadata.get("product", ""),
                    },
                )
                points.append(point)

            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            total_upserted += len(points)

        # Invalidate BM25 index after upsert
        reset_bm25_index()
        self._bm25_initialized = False

        return total_upserted

    def _ensure_bm25_index(self) -> BM25Index:
        """Ensure BM25 index is built from current Qdrant collection.

        Returns:
            Initialized BM25Index instance.
        """
        bm25 = get_bm25_index()

        if not self._bm25_initialized or bm25.index is None:
            logger.info("Building BM25 index from Qdrant collection...")

            # Scroll through all points in the collection
            documents = []
            offset = None

            while True:
                result = self.client.scroll(
                    collection_name=self.collection_name,
                    limit=_QDRANT_SCROLL_BATCH_SIZE,
                    offset=offset,
                    with_payload=True,
                    with_vectors=False,
                )

                points, offset = result

                for point in points:
                    payload = point.payload or {}
                    documents.append(
                        {
                            "id": str(point.id),
                            "content": payload.get("content", ""),
                        }
                    )

                if offset is None:
                    break

            if documents:
                bm25.build_index(documents)
                logger.info(f"BM25 index built with {len(documents)} documents")

            self._bm25_initialized = True

        return bm25

    def _search_vector(self, query: str, top_k: int) -> list[tuple[str, float, dict]]:
        """Perform vector similarity search.

        Args:
            query: Search query.
            top_k: Number of results.

        Returns:
            List of (doc_id, score, payload) tuples.
        """
        query_vector = embed_text(query)

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True,
        )

        results = []
        for point in response.points:
            results.append((str(point.id), point.score, point.payload))

        return results

    def _search_bm25(self, query: str, top_k: int) -> list[tuple[str, float]]:
        """Perform BM25 keyword search.

        Args:
            query: Search query.
            top_k: Number of results.

        Returns:
            List of (doc_id, bm25_score) tuples.
        """
        bm25 = self._ensure_bm25_index()
        return bm25.search(query, top_k)

    def _reciprocal_rank_fusion(
        self,
        vector_results: list[tuple[str, float, dict]],
        bm25_results: list[tuple[str, float]],
        k: int = 60,
    ) -> list[tuple[str, float, dict]]:
        """Combine results using Reciprocal Rank Fusion.

        RRF score = sum(1 / (k + rank)) for each retriever.
        Higher k means more equal weighting between retrievers.

        Args:
            vector_results: Results from vector search (id, score, payload).
            bm25_results: Results from BM25 search (id, score).
            k: RRF constant (default 60).

        Returns:
            Combined results sorted by RRF score (id, rrf_score, payload).
        """
        rrf_scores: dict[str, float] = {}
        payloads: dict[str, dict] = {}

        # Score from vector search
        for rank, (doc_id, _, payload) in enumerate(vector_results):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1 / (k + rank + 1)
            payloads[doc_id] = payload

        # Score from BM25 search
        for rank, (doc_id, _) in enumerate(bm25_results):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1 / (k + rank + 1)

        # For BM25-only results, fetch payload from Qdrant
        missing_payloads = [
            doc_id for doc_id in rrf_scores if doc_id not in payloads
        ]
        if missing_payloads:
            for doc_id in missing_payloads:
                try:
                    points = self.client.retrieve(
                        collection_name=self.collection_name,
                        ids=[doc_id],
                        with_payload=True,
                    )
                    if points:
                        payloads[doc_id] = points[0].payload or {}
                except Exception:
                    payloads[doc_id] = {}

        # Sort by RRF score descending
        sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)

        return [
            (doc_id, rrf_scores[doc_id], payloads.get(doc_id, {}))
            for doc_id in sorted_ids
        ]

    def search(self, query: str, top_k: int | None = None) -> list[Document]:
        """Search for documents using hybrid search (vector + BM25).

        When hybrid search is enabled (RAG_HYBRID_ENABLED=True), combines
        dense vector similarity with BM25 keyword matching using
        Reciprocal Rank Fusion (RRF) for improved retrieval of
        proper nouns and technical terms.

        Args:
            query: The search query string.
            top_k: Maximum number of results to return (default: RAG_TOP_K).

        Returns:
            List of Document objects with content and metadata including score.
        """
        if top_k is None:
            top_k = settings.RAG_TOP_K

        if settings.RAG_HYBRID_ENABLED:
            # Hybrid search: combine vector and BM25 results
            # Fetch more candidates from each retriever for better fusion
            candidates_per_retriever = top_k * 2

            # Expand query with synonyms for better BM25 matching
            expanded_query = expand_query(query)
            if expanded_query != query:
                logger.debug(f"Query expanded: '{query}' -> '{expanded_query}'")

            vector_results = self._search_vector(query, candidates_per_retriever)
            bm25_results = self._search_bm25(expanded_query, candidates_per_retriever)

            # Fuse results using RRF
            fused_results = self._reciprocal_rank_fusion(
                vector_results,
                bm25_results,
                k=settings.RAG_BM25_K,
            )

            # Take top results from fused results
            fused_results = fused_results[:top_k]

            documents = [
                _create_document(payload, rrf_score)
                for _, rrf_score, payload in fused_results
            ]

        else:
            # Pure vector search (original behavior)
            vector_results = self._search_vector(query, top_k)

            documents = [
                _create_document(payload, score)
                for _, score, payload in vector_results
            ]

        return documents
