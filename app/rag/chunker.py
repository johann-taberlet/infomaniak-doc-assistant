"""Text chunking utilities for RAG pipeline."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


def chunk_text(content: str, metadata: dict[str, str]) -> list[Document]:
    """Convert text into document chunks based on configured strategy.

    Strategies:
        - "split": Split text into smaller chunks using RecursiveCharacterTextSplitter.
                   Good for long documents, uses RAG_CHUNK_SIZE and RAG_CHUNK_OVERLAP.
        - "document": Keep entire document as a single chunk.
                      Better for FAQ-style content that's already semantically coherent.

    Args:
        content: The text content to process.
        metadata: Metadata to attach to each chunk.

    Returns:
        List of Document objects with content and metadata.
    """
    if settings.RAG_CHUNK_STRATEGY == "document":
        # Whole document as single chunk - ideal for FAQ-style content
        return [Document(page_content=content, metadata=metadata.copy())]

    # Default: split into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.RAG_CHUNK_SIZE,
        chunk_overlap=settings.RAG_CHUNK_OVERLAP,
        separators=["##", "###", "\n\n", "\n", ". ", " "],
    )

    chunks = text_splitter.split_text(content)

    return [Document(page_content=chunk, metadata=metadata.copy()) for chunk in chunks]
