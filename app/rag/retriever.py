"""Qdrant vector store retriever for RAG pipeline."""

import uuid

from qdrant_client import QdrantClient, models
from langchain_core.documents import Document

from app.config import settings
from app.rag.embeddings import embed_text, embed_documents


class QdrantRetriever:
    """Retriever class for Qdrant vector database operations."""

    def __init__(self) -> None:
        """Initialize the Qdrant client connection."""
        # PRODUCTION: Add retry logic with tenacity and connection health check
        self.client = QdrantClient(url=settings.QDRANT_HOST)
        self.collection_name = settings.QDRANT_COLLECTION

    def create_collection(self, force_recreate: bool = False) -> None:
        """Create the collection if it doesn't exist.

        Uses configurable dimensions (RAG_VECTOR_DIMENSION) and COSINE distance.

        Args:
            force_recreate: If True, delete existing collection and recreate.
        """
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]

        if force_recreate and self.collection_name in collection_names:
            self.client.delete_collection(self.collection_name)
            collection_names.remove(self.collection_name)

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

        return total_upserted

    def search(self, query: str, top_k: int = 5) -> list[Document]:
        """Search for documents similar to the query.

        Args:
            query: The search query string.
            top_k: Maximum number of results to return.

        Returns:
            List of Document objects with content and metadata including score.
        """
        query_vector = embed_text(query)

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True,
        )

        if not response.points:
            return []

        documents = []
        for point in response.points:
            doc = Document(
                page_content=point.payload.get("content", ""),
                metadata={
                    "source": point.payload.get("source", ""),
                    "title": point.payload.get("title", ""),
                    "product": point.payload.get("product", ""),
                    "score": point.score,
                },
            )
            documents.append(doc)

        return documents
