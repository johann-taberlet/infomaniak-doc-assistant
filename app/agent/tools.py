"""LangChain tools for the RAG agent."""

from functools import cache

from langchain.tools import tool

from app.config import settings
from app.rag.retriever import QdrantRetriever


@cache
def get_retriever() -> QdrantRetriever:
    """Get a cached QdrantRetriever instance.

    Uses functools.cache for lazy initialization and connection reuse.
    """
    return QdrantRetriever()


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

    results = []
    for doc in documents:
        title = doc.metadata.get("title", "Untitled")
        source = doc.metadata.get("source", "")
        product = doc.metadata.get("product", "")
        content = doc.page_content

        result = f"**{title}** ({product})\n{content}\nSource: {source}"
        results.append(result)

    return "\n\n---\n\n".join(results)
