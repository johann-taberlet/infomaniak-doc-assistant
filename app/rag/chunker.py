"""Text chunking utilities for RAG pipeline."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings
from app.rag.contextual import add_context_to_chunk, get_product_related_terms


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
        documents = [Document(page_content=content, metadata=metadata.copy())]

        # Apply contextual preprocessing if enabled (v2 architecture)
        if settings.RAG_CONTEXTUAL_ENABLED:
            documents = _apply_contextual_preprocessing(documents, metadata)

        return documents

    # Default: split into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.RAG_CHUNK_SIZE,
        chunk_overlap=settings.RAG_CHUNK_OVERLAP,
        separators=["##", "###", "\n\n", "\n", ". ", " "],
    )

    chunks = text_splitter.split_text(content)

    documents = [Document(page_content=chunk, metadata=metadata.copy()) for chunk in chunks]

    # Apply contextual preprocessing if enabled (v2 architecture)
    if settings.RAG_CONTEXTUAL_ENABLED:
        documents = _apply_contextual_preprocessing(documents, metadata)

    return documents


def _apply_contextual_preprocessing(
    documents: list[Document], metadata: dict[str, str]
) -> list[Document]:
    """Apply contextual preprocessing to documents.

    Prepends document context (title, product, related terms) to each chunk
    for improved embedding quality. Based on Anthropic's Contextual Retrieval technique.

    Args:
        documents: List of Document objects to preprocess.
        metadata: Metadata containing title, product info.

    Returns:
        Documents with contextual prefix added to page_content.
    """
    title = metadata.get("title", "")
    product = metadata.get("product", "")
    related_terms = get_product_related_terms(product) if product else None

    result = []
    for doc in documents:
        contextualized_content = add_context_to_chunk(
            chunk_content=doc.page_content,
            title=title,
            product=product,
            related_terms=related_terms,
        )
        result.append(
            Document(page_content=contextualized_content, metadata=doc.metadata.copy())
        )

    return result
