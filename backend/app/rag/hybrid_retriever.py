"""
Hybrid retriever combining dense and sparse (BM25) search.

Supports:
- Dense-only search (standard vector similarity)
- Sparse-only search (BM25 keyword matching)
- Hybrid search with RRF (Reciprocal Rank Fusion)
"""

import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Any

from langfuse import observe
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models

from backend.app.core.config import settings
from backend.app.rag.chunking import Chunk
from backend.app.rag.embeddings import get_embedding_dimension, get_embeddings
from backend.app.rag.query_processor import QueryProcessor
from backend.app.rag.retriever import RetrievalResult
from backend.app.rag.sparse_embeddings import BM25Embeddings, get_bm25_embeddings


class RetrievalMode(str, Enum):
    """Retrieval mode for hybrid search."""

    DENSE = "dense"
    SPARSE = "sparse"
    HYBRID = "hybrid"


@dataclass
class HybridConfig:
    """Configuration for hybrid retrieval."""

    mode: RetrievalMode = RetrievalMode.HYBRID
    enable_hyde: bool = False
    enable_normalization: bool = False
    rrf_k: int = 60  # RRF constant, industry standard is 60
    dense_weight: float = 0.7  # Weight for dense results in fusion
    sparse_weight: float = 0.3  # Weight for sparse results in fusion

    # Named vectors in Qdrant
    dense_vector_name: str = "dense"
    sparse_vector_name: str = "sparse"


@dataclass
class HybridSearchResult:
    """Result from hybrid search with additional metadata."""

    content: str
    metadata: dict
    score: float
    dense_score: float | None = None
    sparse_score: float | None = None
    context_window: str | None = None

    def to_retrieval_result(self) -> RetrievalResult:
        """Convert to standard RetrievalResult for backward compatibility."""
        return RetrievalResult(
            content=self.content,
            metadata=self.metadata,
            score=self.score,
            context_window=self.context_window,
        )


class HybridRetriever:
    """
    Hybrid retriever combining dense and sparse search.

    Uses Qdrant's native multi-vector support for efficient
    hybrid search with RRF fusion.
    """

    def __init__(
        self,
        collection_name: str,
        config: HybridConfig | None = None,
        host: str | None = None,
        api_key: str | None = None,
    ):
        """
        Initialize hybrid retriever.

        Args:
            collection_name: Name of the Qdrant collection
            config: Hybrid retrieval configuration
            host: Qdrant server URL
            api_key: Qdrant API key
        """
        self.collection_name = collection_name
        self.config = config or HybridConfig()
        self.host = host or settings.qdrant_host
        self.api_key = api_key or settings.qdrant_api_key or None

        # Initialize Qdrant client
        if self.host.startswith("http"):
            self._client = QdrantClient(url=self.host, api_key=self.api_key)
        else:
            self._client = QdrantClient(host=self.host, api_key=self.api_key)

        # Initialize components
        self._dense_embeddings = get_embeddings()
        self._sparse_embeddings: BM25Embeddings | None = None
        self._query_processor: QueryProcessor | None = None

    def _get_sparse_embeddings(self) -> BM25Embeddings:
        """Lazy-load sparse embeddings."""
        if self._sparse_embeddings is None:
            self._sparse_embeddings = get_bm25_embeddings()
        return self._sparse_embeddings

    def _get_query_processor(self) -> QueryProcessor:
        """Lazy-load query processor."""
        if self._query_processor is None:
            self._query_processor = QueryProcessor(
                enable_hyde=self.config.enable_hyde,
                enable_normalization=self.config.enable_normalization,
            )
        return self._query_processor

    def create_collection(
        self,
        dense_vector_size: int | None = None,
        recreate: bool = False,
    ) -> None:
        """
        Create a hybrid collection with both dense and sparse vectors.

        Args:
            dense_vector_size: Dimension of dense vectors (auto-detected if not provided)
            recreate: If True, delete existing collection first
        """
        dense_vector_size = dense_vector_size or get_embedding_dimension()

        # Check if collection exists
        collections = self._client.get_collections()
        exists = any(c.name == self.collection_name for c in collections.collections)

        if exists:
            if recreate:
                self._client.delete_collection(self.collection_name)
            else:
                return

        # Create collection with named vectors
        self._client.create_collection(
            collection_name=self.collection_name,
            vectors_config={
                self.config.dense_vector_name: qdrant_models.VectorParams(
                    size=dense_vector_size,
                    distance=qdrant_models.Distance.COSINE,
                ),
            },
            sparse_vectors_config={
                self.config.sparse_vector_name: qdrant_models.SparseVectorParams(
                    modifier=qdrant_models.Modifier.IDF,
                ),
            },
        )

    def add_chunks(
        self,
        chunks: list[Chunk],
        batch_size: int = 50,
        show_progress: bool = True,
    ) -> int:
        """
        Add chunks with both dense and sparse embeddings.

        Args:
            chunks: List of chunks to add
            batch_size: Number of chunks to process at once
            show_progress: Whether to print progress

        Returns:
            Number of chunks added
        """
        if not chunks:
            return 0

        sparse_embeddings = self._get_sparse_embeddings()
        total_added = 0

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]

            # Get content for embedding
            texts = [chunk.get_embedding_content() for chunk in batch]

            # Generate dense embeddings
            dense_vectors = self._dense_embeddings.embed_documents(texts)

            # Generate sparse embeddings
            # Optionally normalize for BM25
            sparse_texts = texts
            if self.config.enable_normalization:
                processor = self._get_query_processor()
                sparse_texts = [processor.normalize_for_bm25(t) for t in texts]
            sparse_vectors = sparse_embeddings.embed_documents(sparse_texts)

            # Prepare points
            points = []
            for chunk, dense_vec, sparse_vec in zip(batch, dense_vectors, sparse_vectors):
                point_id = str(uuid.uuid4())

                # Prepare payload
                payload: dict[str, Any] = {
                    "content": chunk.content,
                    **chunk.metadata,
                }

                if chunk.context_window:
                    payload["context_window"] = chunk.context_window

                points.append(
                    qdrant_models.PointStruct(
                        id=point_id,
                        vector={
                            self.config.dense_vector_name: dense_vec,
                            self.config.sparse_vector_name: sparse_vec.to_qdrant(),
                        },
                        payload=payload,
                    )
                )

            # Upsert to Qdrant
            self._client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

            total_added += len(batch)

            if show_progress:
                print(f"  Added {total_added}/{len(chunks)} chunks...")

        return total_added

    @observe(name="hybrid_search")
    def search(
        self,
        query: str,
        top_k: int | None = None,
        score_threshold: float | None = None,
        filter_product: str | None = None,
        mode: RetrievalMode | None = None,
    ) -> list[RetrievalResult]:
        """
        Search using configured retrieval mode.

        Args:
            query: Search query
            top_k: Number of results to return
            score_threshold: Minimum similarity score (only for dense)
            filter_product: Filter by product
            mode: Override retrieval mode for this search

        Returns:
            List of retrieval results
        """
        mode = mode or self.config.mode
        top_k = top_k or settings.rag_top_k

        # Build filter
        query_filter = None
        if filter_product:
            query_filter = qdrant_models.Filter(
                must=[
                    qdrant_models.FieldCondition(
                        key="product",
                        match=qdrant_models.MatchValue(value=filter_product),
                    )
                ]
            )

        if mode == RetrievalMode.DENSE:
            return self._search_dense(query, top_k, score_threshold, query_filter)
        elif mode == RetrievalMode.SPARSE:
            return self._search_sparse(query, top_k, query_filter)
        else:  # HYBRID
            return self._search_hybrid(query, top_k, query_filter)

    def _search_dense(
        self,
        query: str,
        top_k: int,
        score_threshold: float | None,
        query_filter: qdrant_models.Filter | None,
    ) -> list[RetrievalResult]:
        """Dense-only search."""
        # Use HyDE if enabled
        search_query = query
        if self.config.enable_hyde:
            processor = self._get_query_processor()
            search_query = processor.generate_hyde_document(query)

        query_vector = self._dense_embeddings.embed_query(search_query)

        response = self._client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            using=self.config.dense_vector_name,
            limit=top_k,
            score_threshold=score_threshold,
            query_filter=query_filter,
            with_payload=True,
        )

        return self._points_to_results(response.points)

    def _search_sparse(
        self,
        query: str,
        top_k: int,
        query_filter: qdrant_models.Filter | None,
    ) -> list[RetrievalResult]:
        """Sparse-only (BM25) search."""
        # Normalize query for BM25 if enabled
        search_query = query
        if self.config.enable_normalization:
            processor = self._get_query_processor()
            search_query = processor.normalize_for_bm25(query)

        sparse_embeddings = self._get_sparse_embeddings()
        query_vector = sparse_embeddings.embed_query(search_query)

        response = self._client.query_points(
            collection_name=self.collection_name,
            query=query_vector.to_qdrant(),
            using=self.config.sparse_vector_name,
            limit=top_k,
            query_filter=query_filter,
            with_payload=True,
        )

        return self._points_to_results(response.points)

    def _search_hybrid(
        self,
        query: str,
        top_k: int,
        query_filter: qdrant_models.Filter | None,
    ) -> list[RetrievalResult]:
        """
        Hybrid search with RRF fusion.

        Uses Qdrant's prefetch for efficient multi-vector retrieval
        and RRF (Reciprocal Rank Fusion) for result merging.
        """
        # Prepare dense query
        dense_query = query
        if self.config.enable_hyde:
            processor = self._get_query_processor()
            dense_query = processor.generate_hyde_document(query)
        dense_vector = self._dense_embeddings.embed_query(dense_query)

        # Prepare sparse query
        sparse_query = query
        if self.config.enable_normalization:
            processor = self._get_query_processor()
            sparse_query = processor.normalize_for_bm25(query)
        sparse_embeddings = self._get_sparse_embeddings()
        sparse_vector = sparse_embeddings.embed_query(sparse_query)

        # Use Qdrant's Query API with prefetch for RRF fusion
        # Prefetch retrieves candidates from each vector type,
        # then fuses using RRF scoring
        prefetch_limit = top_k * 3  # Retrieve more candidates for better fusion

        response = self._client.query_points(
            collection_name=self.collection_name,
            prefetch=[
                qdrant_models.Prefetch(
                    query=dense_vector,
                    using=self.config.dense_vector_name,
                    limit=prefetch_limit,
                ),
                qdrant_models.Prefetch(
                    query=sparse_vector.to_qdrant(),
                    using=self.config.sparse_vector_name,
                    limit=prefetch_limit,
                ),
            ],
            query=qdrant_models.FusionQuery(fusion=qdrant_models.Fusion.RRF),
            query_filter=query_filter,
            with_payload=True,
            limit=top_k,
        )

        return self._points_to_results(response.points)

    def _points_to_results(self, points) -> list[RetrievalResult]:
        """Convert Qdrant points to RetrievalResult objects."""
        results = []
        for point in points:
            payload = point.payload or {}
            results.append(
                RetrievalResult(
                    content=payload.get("content", ""),
                    metadata={k: v for k, v in payload.items() if k not in ("content", "context_window")},
                    score=point.score,
                    context_window=payload.get("context_window"),
                )
            )
        return results

    def get_collection_info(self) -> dict[str, Any]:
        """Get information about the collection."""
        try:
            info = self._client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "points_count": info.points_count,
                "status": str(info.status),
            }
        except Exception as e:
            return {"error": str(e)}

    def collection_exists(self) -> bool:
        """Check if the collection exists."""
        collections = self._client.get_collections()
        return any(c.name == self.collection_name for c in collections.collections)

    def delete_collection(self) -> bool:
        """Delete the collection."""
        try:
            self._client.delete_collection(self.collection_name)
            return True
        except Exception:
            return False
