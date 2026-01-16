"""LangChain tools for the RAG agent."""

from langchain.tools import tool

from app.rag.retriever import QdrantRetriever


@tool(parse_docstring=True)
def search_docs(query: str) -> str:
    """Search the Infomaniak documentation for relevant information.

    Args:
        query: The search query to find relevant documentation.

    Returns:
        Formatted search results with content and source citations.
    """
    retriever = QdrantRetriever()
    documents = retriever.search(query, top_k=5)

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
