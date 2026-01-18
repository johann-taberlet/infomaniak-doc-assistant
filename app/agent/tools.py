"""LangChain tools for the RAG agent."""

from contextvars import ContextVar
from functools import cache
from typing import Any

from langchain.tools import tool

from app.config import settings
from app.models.schemas import SourceDocument
from app.rag.retriever import QdrantRetriever


@cache
def get_retriever() -> QdrantRetriever:
    """Get a cached QdrantRetriever instance.

    Uses functools.cache for lazy initialization and connection reuse.
    """
    return QdrantRetriever()


# Context variable for request-scoped source storage
_sources_var: ContextVar[list[dict[str, Any]]] = ContextVar("sources", default=[])


def get_sources() -> list[dict[str, Any]]:
    """Get current sources list (creates new list if not set)."""
    try:
        return _sources_var.get()
    except LookupError:
        sources: list[dict[str, Any]] = []
        _sources_var.set(sources)
        return sources


def add_source(source: dict[str, Any]) -> None:
    """Add a source to the current request."""
    sources = get_sources()
    sources.append(source)


def reset_context() -> None:
    """Reset all context variables for a new request."""
    _sources_var.set([])


# Maximum number of sources to show in the UI cards (top N most relevant)
MAX_UI_SOURCES = 4
# Maximum length for source snippets in UI
_MAX_SNIPPET_LENGTH = 150


@tool(parse_docstring=True)
def search_docs(query: str) -> str:
    """Search the Infomaniak documentation for relevant information.

    Args:
        query: The search query to find relevant documentation.

    Returns:
        Formatted search results with content and source citations.
    """
    retriever = get_retriever()
    documents = retriever.search(query, top_k=settings.RAG_TOP_K)

    if not documents:
        return "No relevant documentation found for this query."

    # Build sources for UI (stored separately, emitted last)
    results = []
    seen_titles: set[str] = set()

    for doc in documents:
        title = doc.metadata.get("title", "Untitled")
        source = doc.metadata.get("source", "")
        product = doc.metadata.get("product", "")
        content = doc.page_content
        score = doc.metadata.get("score")

        # Add to text results (all documents for LLM context)
        result = f"**{title}** ({product})\n{content}\nSource: {source}"
        results.append(result)

        # Build source document for UI (deduplicated by title, limited count)
        if len(get_sources()) < MAX_UI_SOURCES and title not in seen_titles:
            seen_titles.add(title)
            snippet = content[:_MAX_SNIPPET_LENGTH] + "..." if len(content) > _MAX_SNIPPET_LENGTH else content
            source_doc = SourceDocument(
                title=title,
                product=product or "Infomaniak",
                url=source,
                snippet=snippet,
                relevance_score=score,
            )
            add_source(source_doc.model_dump(by_alias=True))

    return "\n\n---\n\n".join(results)
