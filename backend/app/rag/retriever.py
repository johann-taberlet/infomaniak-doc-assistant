"""
Qdrant retriever for vector similarity search.

Provides a simple interface for storing and retrieving documents
from Qdrant vector database.
"""

import uuid
from dataclasses import dataclass
from typing import Any

from langfuse import observe
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models

from backend.app.core.config import settings
from backend.app.rag.chunking import Chunk
from backend.app.rag.embeddings import get_embedding_dimension, get_embeddings


@dataclass
class RetrievalResult:
    """Result from a retrieval query."""

    content: str
    metadata: dict
    score: float
    context_window: str | None = None


class QdrantRetriever:
    """
    Qdrant-based retriever for vector similarity search.

    Handles:
    - Collection creation with proper configuration
    - Document/chunk storage with embeddings
    - Similarity search with optional filtering
    """

    def __init__(
        self,
        collection_name: str | None = None,
        host: str | None = None,
        api_key: str | None = None,
    ):
        """
        Initialize Qdrant retriever.

        Args:
            collection_name: Name of the Qdrant collection
            host: Qdrant server URL
            api_key: Qdrant API key (optional for local)
        """
        self.collection_name = collection_name or settings.qdrant_collection
        self.host = host or settings.qdrant_host
        self.api_key = api_key or settings.qdrant_api_key or None

        # Initialize client
        if self.host.startswith("http"):
            # URL-based connection
            self._client = QdrantClient(url=self.host, api_key=self.api_key)
        else:
            # Host:port connection
            self._client = QdrantClient(host=self.host, api_key=self.api_key)

        # Embeddings provider
        self._embeddings = get_embeddings()

    def create_collection(
        self,
        vector_size: int | None = None,
        distance: str = "Cosine",
        recreate: bool = False,
    ) -> None:
        """
        Create or recreate a Qdrant collection.

        Args:
            vector_size: Dimension of vectors (auto-detected if not provided)
            distance: Distance metric (Cosine, Euclid, Dot)
            recreate: If True, delete existing collection first
        """
        vector_size = vector_size or get_embedding_dimension()

        # Check if collection exists
        collections = self._client.get_collections()
        exists = any(c.name == self.collection_name for c in collections.collections)

        if exists:
            if recreate:
                self._client.delete_collection(self.collection_name)
            else:
                return  # Collection already exists

        # Create collection
        distance_map = {
            "Cosine": qdrant_models.Distance.COSINE,
            "Euclid": qdrant_models.Distance.EUCLID,
            "Dot": qdrant_models.Distance.DOT,
        }

        self._client.create_collection(
            collection_name=self.collection_name,
            vectors_config=qdrant_models.VectorParams(
                size=vector_size,
                distance=distance_map.get(distance, qdrant_models.Distance.COSINE),
            ),
        )

    def add_chunks(
        self,
        chunks: list[Chunk],
        batch_size: int = 100,
        show_progress: bool = True,
    ) -> int:
        """
        Add chunks to the collection.

        Args:
            chunks: List of chunks to add
            batch_size: Number of chunks to process at once
            show_progress: Whether to print progress

        Returns:
            Number of chunks added
        """
        if not chunks:
            return 0

        total_added = 0

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]

            # Get content for embedding (may include context window)
            texts = [chunk.get_embedding_content() for chunk in batch]

            # Generate embeddings
            embeddings = self._embeddings.embed_documents(texts)

            # Prepare points
            points = []
            for chunk, embedding in zip(batch, embeddings):
                point_id = str(uuid.uuid4())

                # Prepare payload
                payload: dict[str, Any] = {
                    "content": chunk.content,
                    **chunk.metadata,
                }

                # Store context window if present
                if chunk.context_window:
                    payload["context_window"] = chunk.context_window

                points.append(
                    qdrant_models.PointStruct(
                        id=point_id,
                        vector=embedding,
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

    @observe(name="retrieval")
    def search(
        self,
        query: str,
        top_k: int | None = None,
        score_threshold: float | None = None,
        filter_product: str | None = None,
    ) -> list[RetrievalResult]:
        """
        Search for similar documents.

        Args:
            query: Search query
            top_k: Number of results to return
            score_threshold: Minimum similarity score
            filter_product: Filter by product (kdrive, kmeet, kchat)

        Returns:
            List of retrieval results
        """
        top_k = top_k or settings.rag_top_k
        score_threshold = score_threshold or settings.rag_similarity_threshold

        # Generate query embedding
        query_embedding = self._embeddings.embed_query(query)

        # Build filter if needed
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

        # Search using query_points (newer qdrant-client API)
        response = self._client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=top_k,
            score_threshold=score_threshold,
            query_filter=query_filter,
            with_payload=True,
        )

        # Convert to RetrievalResult
        retrieval_results = []
        for point in response.points:
            payload = point.payload or {}
            retrieval_results.append(
                RetrievalResult(
                    content=payload.get("content", ""),
                    metadata={k: v for k, v in payload.items() if k != "content"},
                    score=point.score,
                    context_window=payload.get("context_window"),
                )
            )

        return retrieval_results

    def get_collection_info(self) -> dict[str, Any]:
        """Get information about the collection."""
        try:
            info = self._client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status,
            }
        except Exception as e:
            return {"error": str(e)}

    def delete_collection(self) -> bool:
        """Delete the collection."""
        try:
            self._client.delete_collection(self.collection_name)
            return True
        except Exception:
            return False

    def collection_exists(self) -> bool:
        """Check if the collection exists."""
        collections = self._client.get_collections()
        return any(c.name == self.collection_name for c in collections.collections)
