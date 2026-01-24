"""
Chunking strategies for document processing.

Each strategy implements a different approach to splitting documents into chunks
for embedding and retrieval. The choice of strategy affects RAG quality.
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Literal

from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass
class Document:
    """A document with content and metadata."""

    content: str
    metadata: dict = field(default_factory=dict)

    @property
    def page_content(self) -> str:
        """Alias for content to match LangChain interface."""
        return self.content


@dataclass
class Chunk:
    """A chunk of a document with content, metadata, and optional context."""

    content: str
    metadata: dict = field(default_factory=dict)
    # For sentence window: the larger context window
    context_window: str | None = None

    @property
    def page_content(self) -> str:
        """Alias for content to match LangChain interface."""
        return self.content

    def get_embedding_content(self) -> str:
        """Get content to use for embedding (may include context window)."""
        if self.context_window:
            return self.context_window
        return self.content


ChunkingStrategy = Literal["full_document", "recursive", "semantic", "sentence_window"]


class BaseChunker(ABC):
    """Abstract base class for chunking strategies."""

    @abstractmethod
    def chunk(self, documents: list[Document]) -> list[Chunk]:
        """Split documents into chunks."""
        ...

    def _extract_metadata(self, content: str, source_path: str = "") -> dict:
        """Extract metadata from document content."""
        metadata = {
            "source": source_path,
            "title": "",
            "source_url": "",
            "product": "",
            "faq_id": "",
        }

        lines = content.split("\n")

        # Extract title (first # heading)
        for line in lines:
            if line.startswith("# "):
                metadata["title"] = line[2:].strip()
                break

        # Extract source URL
        for line in lines:
            if line.startswith("Source:"):
                url = line.replace("Source:", "").strip()
                metadata["source_url"] = url
                # Extract FAQ ID from URL
                match = re.search(r"/faq/(\d+)/", url)
                if match:
                    metadata["faq_id"] = match.group(1)
                break

        # Infer product from URL or title
        source_lower = metadata["source_url"].lower()
        title_lower = metadata["title"].lower()
        if "kdrive" in source_lower or "kdrive" in title_lower:
            metadata["product"] = "kdrive"
        elif "kmeet" in source_lower or "kmeet" in title_lower:
            metadata["product"] = "kmeet"
        elif "kchat" in source_lower or "kchat" in title_lower:
            metadata["product"] = "kchat"

        return metadata


class FullDocumentChunker(BaseChunker):
    """
    No splitting - each document becomes one chunk.

    Best for:
    - Short documents (like FAQ entries)
    - When full context is important
    - Baseline comparison

    Pros:
    - Preserves complete context
    - No information loss at chunk boundaries
    - Simple and predictable

    Cons:
    - May exceed embedding model context limits
    - Retrieves entire documents (less precise)
    """

    def chunk(self, documents: list[Document]) -> list[Chunk]:
        """Return each document as a single chunk."""
        chunks = []
        for doc in documents:
            metadata = self._extract_metadata(doc.content, doc.metadata.get("source", ""))
            metadata.update(doc.metadata)
            chunks.append(Chunk(content=doc.content, metadata=metadata))
        return chunks


class RecursiveChunker(BaseChunker):
    """
    Standard recursive character text splitting.

    Uses hierarchical separators to split text while trying to preserve
    semantic boundaries (paragraphs > sentences > words).

    Best for:
    - General-purpose chunking
    - Documents with varied structure
    - When chunk size control is important

    Pros:
    - Configurable chunk size
    - Respects natural boundaries
    - Well-tested approach

    Cons:
    - May split mid-section
    - Fixed chunk size may not align with semantic units
    """

    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # FAQ-aware separators: prefer splitting at headings, then paragraphs, etc.
        self.separators = ["\n## ", "\n### ", "\n\n", "\n", " ", ""]

    def chunk(self, documents: list[Document]) -> list[Chunk]:
        """Split documents using recursive character splitting."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
            length_function=len,
            is_separator_regex=False,
        )

        chunks = []
        for doc in documents:
            base_metadata = self._extract_metadata(doc.content, doc.metadata.get("source", ""))
            base_metadata.update(doc.metadata)

            # Split the document
            text_chunks = splitter.split_text(doc.content)

            for i, text in enumerate(text_chunks):
                chunk_metadata = {
                    **base_metadata,
                    "chunk_index": i,
                    "total_chunks": len(text_chunks),
                }
                chunks.append(Chunk(content=text, metadata=chunk_metadata))

        return chunks


class SemanticChunker(BaseChunker):
    """
    Split by markdown headings, keeping sections intact.

    Each ## or ### section becomes a chunk, preserving the logical
    structure of the documentation.

    Best for:
    - Well-structured markdown documents
    - FAQ-style content with clear sections
    - When semantic boundaries are important

    Pros:
    - Preserves semantic units
    - Natural alignment with document structure
    - Context within each section is complete

    Cons:
    - Variable chunk sizes
    - Very long sections may still need splitting
    """

    def __init__(self, max_chunk_size: int = 3000, include_title: bool = True):
        self.max_chunk_size = max_chunk_size
        self.include_title = include_title

    def chunk(self, documents: list[Document]) -> list[Chunk]:
        """Split documents by markdown headings."""
        chunks = []

        for doc in documents:
            base_metadata = self._extract_metadata(doc.content, doc.metadata.get("source", ""))
            base_metadata.update(doc.metadata)

            sections = self._split_by_headings(doc.content)

            for i, (heading, content) in enumerate(sections):
                # Include document title and heading for context
                if self.include_title and base_metadata.get("title"):
                    chunk_content = f"# {base_metadata['title']}\n\n"
                    if heading and not heading.startswith("# "):
                        chunk_content += f"{heading}\n\n"
                    chunk_content += content
                else:
                    chunk_content = f"{heading}\n\n{content}" if heading else content

                # If section is too long, fall back to recursive splitting
                if len(chunk_content) > self.max_chunk_size:
                    sub_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=self.max_chunk_size,
                        chunk_overlap=100,
                        separators=["\n\n", "\n", " ", ""],
                    )
                    sub_chunks = sub_splitter.split_text(chunk_content)
                    for j, sub_content in enumerate(sub_chunks):
                        chunk_metadata = {
                            **base_metadata,
                            "section": heading,
                            "section_index": i,
                            "sub_chunk_index": j,
                        }
                        chunks.append(Chunk(content=sub_content, metadata=chunk_metadata))
                else:
                    chunk_metadata = {
                        **base_metadata,
                        "section": heading,
                        "section_index": i,
                    }
                    chunks.append(Chunk(content=chunk_content, metadata=chunk_metadata))

        return chunks

    def _split_by_headings(self, content: str) -> list[tuple[str, str]]:
        """
        Split content by ## and ### headings.

        Returns list of (heading, content) tuples.
        """
        # Pattern to match ## or ### headings
        heading_pattern = re.compile(r"^(#{2,3}\s+.+)$", re.MULTILINE)

        sections: list[tuple[str, str]] = []
        last_end = 0
        last_heading = ""

        for match in heading_pattern.finditer(content):
            # Capture content before this heading
            if match.start() > last_end:
                section_content = content[last_end : match.start()].strip()
                if section_content:
                    sections.append((last_heading, section_content))

            last_heading = match.group(1)
            last_end = match.end()

        # Capture remaining content after last heading
        if last_end < len(content):
            remaining = content[last_end:].strip()
            if remaining:
                sections.append((last_heading, remaining))

        # If no headings found, return whole document
        if not sections:
            sections.append(("", content))

        return sections


class SentenceWindowChunker(BaseChunker):
    """
    Small chunks with larger context windows for retrieval.

    Creates sentence-level chunks but embeds them with surrounding context.
    At retrieval time, returns the small chunk but includes the larger
    context window for the LLM.

    Best for:
    - Fine-grained retrieval
    - When precise answer location matters
    - Hybrid approaches

    Pros:
    - Very precise retrieval
    - LLM gets rich context
    - Good for extractive QA

    Cons:
    - More chunks to embed and store
    - Increased complexity
    - May fragment coherent sections
    """

    def __init__(self, window_size: int = 3, sentence_overlap: int = 1):
        """
        Initialize sentence window chunker.

        Args:
            window_size: Number of sentences to include in context window
            sentence_overlap: Number of sentences to overlap between chunks
        """
        self.window_size = window_size
        self.sentence_overlap = sentence_overlap

    def chunk(self, documents: list[Document]) -> list[Chunk]:
        """Split documents into sentences with context windows."""
        chunks = []

        for doc in documents:
            base_metadata = self._extract_metadata(doc.content, doc.metadata.get("source", ""))
            base_metadata.update(doc.metadata)

            sentences = self._split_into_sentences(doc.content)

            if not sentences:
                continue

            # Create chunks with sliding window
            step = max(1, self.window_size - self.sentence_overlap)
            for i in range(0, len(sentences), step):
                # Current chunk: window_size sentences
                chunk_sentences = sentences[i : i + self.window_size]
                chunk_content = " ".join(chunk_sentences)

                # Context window: extended context around the chunk
                context_start = max(0, i - self.window_size)
                context_end = min(len(sentences), i + self.window_size * 2)
                context_sentences = sentences[context_start:context_end]
                context_window = " ".join(context_sentences)

                chunk_metadata = {
                    **base_metadata,
                    "sentence_start": i,
                    "sentence_end": min(i + self.window_size, len(sentences)),
                    "context_start": context_start,
                    "context_end": context_end,
                }

                chunks.append(
                    Chunk(
                        content=chunk_content,
                        metadata=chunk_metadata,
                        context_window=context_window,
                    )
                )

        return chunks

    def _split_into_sentences(self, text: str) -> list[str]:
        """
        Split text into sentences.

        Uses a simple regex-based approach that handles common cases.
        """
        # Remove code blocks (preserve as single "sentence")
        code_blocks: list[str] = []

        def preserve_code(match: re.Match[str]) -> str:
            code_blocks.append(match.group(0))
            return f"__CODE_BLOCK_{len(code_blocks) - 1}__"

        text = re.sub(r"```[\s\S]*?```", preserve_code, text)

        # Split on sentence boundaries
        # Handles: . ! ? followed by space or newline
        sentence_pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])\n+")
        sentences = sentence_pattern.split(text)

        # Restore code blocks
        result = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            # Restore code blocks
            for i, code in enumerate(code_blocks):
                sentence = sentence.replace(f"__CODE_BLOCK_{i}__", code)
            result.append(sentence)

        return result


def get_chunker(
    strategy: ChunkingStrategy,
    chunk_size: int = 1500,
    chunk_overlap: int = 200,
    window_size: int = 3,
) -> BaseChunker:
    """
    Factory function to get a chunker by strategy name.

    Args:
        strategy: Name of the chunking strategy
        chunk_size: Size of chunks (for recursive strategy)
        chunk_overlap: Overlap between chunks (for recursive strategy)
        window_size: Sentence window size (for sentence_window strategy)

    Returns:
        Configured chunker instance
    """
    chunkers: dict[ChunkingStrategy, BaseChunker] = {
        "full_document": FullDocumentChunker(),
        "recursive": RecursiveChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap),
        "semantic": SemanticChunker(max_chunk_size=chunk_size * 2),
        "sentence_window": SentenceWindowChunker(window_size=window_size),
    }

    if strategy not in chunkers:
        raise ValueError(
            f"Unknown chunking strategy: {strategy}. "
            f"Available: {list(chunkers.keys())}"
        )

    return chunkers[strategy]
