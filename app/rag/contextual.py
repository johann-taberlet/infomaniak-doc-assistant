"""Contextual retrieval preprocessing.

Prepends document context to chunks before embedding to improve
retrieval quality. Based on Anthropic's Contextual Retrieval technique
which shows 35-67% reduction in retrieval failures.

The idea is that chunks often lose context when split from their parent
document. By prepending the document title, product, and related terms,
the embedding captures the full semantic meaning.
"""


def add_context_to_chunk(
    chunk_content: str,
    title: str,
    product: str,
    section_header: str | None = None,
    related_terms: list[str] | None = None,
) -> str:
    """Add contextual prefix to chunk for better embeddings.

    Args:
        chunk_content: Original chunk text
        title: Document title (e.g., "How to share files on kDrive")
        product: Product name (e.g., "kdrive", "kmeet", "kchat")
        section_header: Optional section heading within the document
        related_terms: Optional list of related search terms/synonyms

    Returns:
        Chunk with contextual prefix prepended

    Example:
        Input: "Click the share button to generate a public link."
        Output: "KDRIVE > How to share files on kDrive

                Related terms: public link, share data, file sharing

                Click the share button to generate a public link."
    """
    context_parts = []

    # Product and title context
    if product and title:
        context_parts.append(f"{product.upper()} > {title}")
    elif title:
        context_parts.append(title)
    elif product:
        context_parts.append(product.upper())

    # Section context (if splitting within document)
    if section_header:
        context_parts.append(f"> {section_header}")

    # Build context header
    context_header = " ".join(context_parts) if context_parts else ""

    # Add related terms for better keyword matching
    related_line = ""
    if related_terms:
        related_line = f"\nRelated terms: {', '.join(related_terms)}"

    # Combine context with original content
    if context_header or related_line:
        return f"{context_header}{related_line}\n\n{chunk_content}"

    return chunk_content


def get_product_related_terms(product: str) -> list[str]:
    """Get common related terms for a product.

    These help with synonym matching in embeddings.

    Args:
        product: Product name (kdrive, kmeet, kchat)

    Returns:
        List of related terms for the product
    """
    product_terms = {
        "kdrive": [
            "cloud storage",
            "file sync",
            "file sharing",
            "online drive",
            "backup",
        ],
        "kmeet": [
            "video conference",
            "meeting",
            "video call",
            "screen share",
            "webinar",
        ],
        "kchat": [
            "team chat",
            "messaging",
            "instant messaging",
            "collaboration",
            "channels",
        ],
    }

    return product_terms.get(product.lower(), [])
