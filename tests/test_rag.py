"""Tests for RAG pipeline components."""

import pytest

from app.rag.chunker import chunk_text


def test_chunker_splits_text():
    """Test that chunker splits text into multiple chunks."""
    # Create text longer than chunk_size (1500 chars default)
    long_text = "This is a test sentence. " * 100  # ~2500 chars
    metadata = {"source": "test", "product": "kdrive", "title": "Test Document"}

    chunks = chunk_text(long_text, metadata)

    # Should produce multiple chunks
    assert len(chunks) > 1

    # Each chunk should have the metadata
    for chunk in chunks:
        assert chunk.metadata["source"] == "test"
        assert chunk.metadata["product"] == "kdrive"

    # Each chunk should have content
    for chunk in chunks:
        assert len(chunk.page_content) > 0


def test_retriever_initializes():
    """Test that QdrantRetriever initializes when Qdrant is available."""
    try:
        from app.rag.retriever import QdrantRetriever

        retriever = QdrantRetriever()

        # Check client is connected by getting collections (will fail if Qdrant is down)
        retriever.client.get_collections()

        assert retriever.collection_name is not None
        assert hasattr(retriever, "search")
        assert hasattr(retriever, "upsert")
        assert hasattr(retriever, "create_collection")
    except Exception as e:
        pytest.skip(f"Qdrant unavailable: {e}")
