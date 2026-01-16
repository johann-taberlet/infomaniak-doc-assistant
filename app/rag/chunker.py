"""Text chunking utilities for RAG pipeline."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


def chunk_text(content: str, metadata: dict[str, str]) -> list[Document]:
    """Split text into chunks with metadata.

    Uses configurable chunk size and overlap from settings.
    Default: 1500 chars with 200 overlap for better context preservation.

    Args:
        content: The text content to chunk.
        metadata: Metadata to attach to each chunk.

    Returns:
        List of Document objects with content and metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.RAG_CHUNK_SIZE,
        chunk_overlap=settings.RAG_CHUNK_OVERLAP,
        separators=["##", "###", "\n\n", "\n", ". ", " "],
    )

    chunks = text_splitter.split_text(content)

    return [Document(page_content=chunk, metadata=metadata.copy()) for chunk in chunks]
