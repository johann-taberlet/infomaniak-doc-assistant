"""Text chunking utilities for RAG pipeline."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


def chunk_text(content: str, metadata: dict[str, str]) -> list[Document]:
    """Convert text into document chunks using RecursiveCharacterTextSplitter.

    Args:
        content: The text content to process.
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
