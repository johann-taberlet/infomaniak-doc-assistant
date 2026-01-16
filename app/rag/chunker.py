"""Text chunking utilities for RAG pipeline."""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def chunk_text(content: str, metadata: dict[str, str]) -> list[Document]:
    """Split text into chunks with metadata.

    Args:
        content: The text content to chunk.
        metadata: Metadata to attach to each chunk.

    Returns:
        List of Document objects with content and metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["##", "###", "\n\n", "\n", ". ", " "],
    )

    chunks = text_splitter.split_text(content)

    return [
        Document(page_content=chunk, metadata=metadata.copy())
        for chunk in chunks
    ]
