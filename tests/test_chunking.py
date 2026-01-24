"""
Tests for chunking strategies.

These tests validate our evaluation-based decision to use full_document chunking
and ensure metadata extraction works correctly for filtering.
"""

import pytest

from backend.app.rag.chunking import (
    Chunk,
    Document,
    FullDocumentChunker,
    RecursiveChunker,
    get_chunker,
)


# Sample FAQ document matching real data structure
SAMPLE_FAQ = """# How to share a file in kDrive

Source: https://www.infomaniak.com/en/support/faq/2847/share-file-kdrive

To share a file in kDrive, follow these steps:

1. Open kDrive web app
2. Right-click on the file
3. Select "Share"

## Share options

You can share with:
- Specific users
- Anyone with the link

## Permissions

Choose between:
- View only
- Edit access
"""


class TestFullDocumentChunker:
    """Tests for the evaluation-winning full_document strategy."""

    def test_preserves_entire_document(self):
        """Full document chunking should return exactly one chunk per document."""
        doc = Document(content=SAMPLE_FAQ, metadata={"source": "test.md"})
        chunker = FullDocumentChunker()

        chunks = chunker.chunk([doc])

        assert len(chunks) == 1
        assert chunks[0].content == SAMPLE_FAQ

    def test_extracts_title(self):
        """Should extract title from first # heading."""
        doc = Document(content=SAMPLE_FAQ)
        chunker = FullDocumentChunker()

        chunks = chunker.chunk([doc])

        assert chunks[0].metadata["title"] == "How to share a file in kDrive"

    def test_extracts_source_url(self):
        """Should extract source URL from Source: line."""
        doc = Document(content=SAMPLE_FAQ)
        chunker = FullDocumentChunker()

        chunks = chunker.chunk([doc])

        assert chunks[0].metadata["source_url"] == "https://www.infomaniak.com/en/support/faq/2847/share-file-kdrive"

    def test_extracts_faq_id(self):
        """Should extract FAQ ID from URL pattern."""
        doc = Document(content=SAMPLE_FAQ)
        chunker = FullDocumentChunker()

        chunks = chunker.chunk([doc])

        assert chunks[0].metadata["faq_id"] == "2847"

    def test_infers_product_from_url(self):
        """Should infer product (kdrive/kmeet/kchat) from URL."""
        doc = Document(content=SAMPLE_FAQ)
        chunker = FullDocumentChunker()

        chunks = chunker.chunk([doc])

        assert chunks[0].metadata["product"] == "kdrive"

    def test_handles_kmeet_product(self):
        """Should correctly identify kMeet product."""
        kmeet_faq = """# Start a kMeet video call

Source: https://www.infomaniak.com/en/support/faq/1234/start-kmeet-call

Instructions here.
"""
        doc = Document(content=kmeet_faq)
        chunker = FullDocumentChunker()

        chunks = chunker.chunk([doc])

        assert chunks[0].metadata["product"] == "kmeet"

    def test_handles_multiple_documents(self):
        """Should process multiple documents independently."""
        docs = [
            Document(content="# Doc 1\n\nContent 1"),
            Document(content="# Doc 2\n\nContent 2"),
        ]
        chunker = FullDocumentChunker()

        chunks = chunker.chunk(docs)

        assert len(chunks) == 2
        assert chunks[0].metadata["title"] == "Doc 1"
        assert chunks[1].metadata["title"] == "Doc 2"


class TestRecursiveChunker:
    """Tests for recursive chunking (used in evaluation comparison)."""

    def test_splits_long_documents(self):
        """Should split documents exceeding chunk_size."""
        long_content = "This is a sentence. " * 200  # ~4000 chars
        doc = Document(content=long_content)
        chunker = RecursiveChunker(chunk_size=500, chunk_overlap=50)

        chunks = chunker.chunk([doc])

        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk.content) <= 600  # Allow some buffer

    def test_preserves_metadata_across_chunks(self):
        """Each chunk should retain document metadata."""
        long_content = f"# Test Document\n\nSource: https://example.com/faq/123/test\n\n{'Content. ' * 200}"
        doc = Document(content=long_content)
        chunker = RecursiveChunker(chunk_size=500)

        chunks = chunker.chunk([doc])

        for chunk in chunks:
            assert chunk.metadata["title"] == "Test Document"
            assert chunk.metadata["faq_id"] == "123"

    def test_adds_chunk_index_metadata(self):
        """Should add chunk_index and total_chunks metadata."""
        long_content = "Sentence. " * 200
        doc = Document(content=long_content)
        chunker = RecursiveChunker(chunk_size=500)

        chunks = chunker.chunk([doc])

        for i, chunk in enumerate(chunks):
            assert chunk.metadata["chunk_index"] == i
            assert chunk.metadata["total_chunks"] == len(chunks)


class TestChunkerFactory:
    """Tests for the get_chunker factory function."""

    def test_returns_full_document_chunker(self):
        """Should return FullDocumentChunker for 'full_document' strategy."""
        chunker = get_chunker("full_document")
        assert isinstance(chunker, FullDocumentChunker)

    def test_returns_recursive_chunker(self):
        """Should return RecursiveChunker for 'recursive' strategy."""
        chunker = get_chunker("recursive", chunk_size=1000)
        assert isinstance(chunker, RecursiveChunker)

    def test_raises_for_unknown_strategy(self):
        """Should raise ValueError for unknown strategy."""
        with pytest.raises(ValueError, match="Unknown chunking strategy"):
            get_chunker("nonexistent")  # type: ignore


class TestChunkDataclass:
    """Tests for the Chunk dataclass."""

    def test_get_embedding_content_without_context_window(self):
        """Should return content when no context_window."""
        chunk = Chunk(content="test content")
        assert chunk.get_embedding_content() == "test content"

    def test_get_embedding_content_with_context_window(self):
        """Should return context_window when present (sentence window strategy)."""
        chunk = Chunk(content="short", context_window="longer context window")
        assert chunk.get_embedding_content() == "longer context window"
