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
        self.client = QdrantClient(url=settings.QDRANT_HOST)
        self.collection_name = settings.QDRANT_COLLECTION

    def create_collection(self) -> None:
        """Create the collection if it doesn't exist.

        Uses 768 dimensions for nomic-embed-text embeddings and COSINE distance.
        """
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]

        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=768,
                    distance=models.Distance.COSINE,
                ),
            )

    def upsert(self, chunks: list[Document]) -> int:
        """Upsert document chunks into the collection.

        Args:
            chunks: List of Document objects with page_content and metadata.

        Returns:
            Number of points upserted.
        """
        if not chunks:
            return 0

        # Extract texts and embed them
        texts = [chunk.page_content for chunk in chunks]
        vectors = embed_documents(texts)

        # Build points with unique IDs
        points = []
        for chunk, vector in zip(chunks, vectors):
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

        return len(points)

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
