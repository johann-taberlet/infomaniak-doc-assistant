"""Tools for the ReAct pattern prototype.

All output happens through tool calls - no direct text output from the model.
This enables true interleaving of text and UI components.
"""

import json
import re
from contextvars import ContextVar
from functools import cache
from typing import Any

from langchain.tools import tool

from app.config import settings
from app.rag.retriever import QdrantRetriever


def strip_markdown(text: str) -> str:
    """Remove markdown formatting from text for clean snippets."""
    # Remove headers
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    # Remove bold/italic
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove code blocks
    text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Remove bullet points
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    # Remove numbered lists
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    # Collapse whitespace
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Request-scoped storage using contextvars (thread-safe, async-safe)
_segments_var: ContextVar[list[dict[str, Any]]] = ContextVar("segments", default=[])
_sources_var: ContextVar[list[dict[str, Any]]] = ContextVar("sources", default=[])


@cache
def get_retriever() -> QdrantRetriever:
    """Get a cached QdrantRetriever instance."""
    return QdrantRetriever()


def reset_segments() -> None:
    """Reset segments and sources for a new request."""
    _segments_var.set([])
    _sources_var.set([])


def get_segments() -> list[dict[str, Any]]:
    """Get all accumulated segments."""
    return _segments_var.get().copy()


def pop_segment() -> dict[str, Any] | None:
    """Pop the next segment from the queue."""
    segments = _segments_var.get()
    if segments:
        return segments.pop(0)
    return None


def get_sources() -> list[dict[str, Any]]:
    """Get all accumulated sources."""
    return _sources_var.get().copy()


def add_segment(segment: dict[str, Any]) -> None:
    """Add a segment to the accumulator."""
    _segments_var.get().append(segment)


def add_sources(sources: list[dict[str, Any]]) -> None:
    """Add sources to the accumulator."""
    _sources_var.get().extend(sources)


@tool(parse_docstring=True)
def render_text(order: int, content: str) -> str:
    """Output a text segment to the user.

    Use this tool to write paragraphs, introductions, conclusions, or any prose.
    Call this multiple times to build your response piece by piece.
    You MUST use this tool for ALL text output - do NOT output raw text.

    Args:
        order: Display order number starting from 1. Use sequential numbers.
        content: The markdown text to display to the user.

    Returns:
        Confirmation that the text was rendered.
    """
    add_segment({"type": "text", "content": content, "order": order})
    return f"Text segment rendered ({len(content)} chars) at position {order}"


@tool(parse_docstring=True)
def render_steps(order: int, title: str, steps_json: str) -> str:
    """Render an interactive step-by-step guide.

    Use this when explaining how to do something with multiple steps.
    The user will see an interactive checklist they can mark as complete.

    Args:
        order: Display order number starting from 1. Use sequential numbers.
        title: The title of the guide, e.g. "How to create a Drop Box".
        steps_json: JSON array where each object has number, title, description fields.

    Returns:
        Confirmation that the step guide was rendered.
    """
    try:
        steps = json.loads(steps_json)
        add_segment({"type": "step_guide", "title": title, "steps": steps, "order": order})
        return f"Step guide '{title}' rendered with {len(steps)} steps at position {order}"
    except json.JSONDecodeError as e:
        return f"Error parsing steps_json: {e}. Please provide valid JSON."


@tool(parse_docstring=True)
def render_platform_availability(order: int, feature: str, platforms_json: str) -> str:
    """Render a visual grid showing feature availability across platforms.

    Use this when discussing platform-specific limitations or availability.

    Args:
        order: Display order number starting from 1. Use sequential numbers.
        feature: The feature name, e.g. "Lite Sync" or "Drop Box".
        platforms_json: JSON array where each object has platform and availability fields.

    Returns:
        Confirmation that platform availability was rendered.
    """
    try:
        platforms = json.loads(platforms_json)
        add_segment({"type": "platform_availability", "feature": feature, "platforms": platforms, "order": order})
        return f"Platform availability for '{feature}' rendered at position {order}"
    except json.JSONDecodeError as e:
        return f"Error parsing platforms_json: {e}. Please provide valid JSON."


@tool(parse_docstring=True)
def render_quick_actions(order: int, actions_json: str) -> str:
    """Render contextual quick action buttons.

    Use this to provide helpful follow-up actions like opening documentation,
    contacting support, or links to related features. Great for giving users
    next steps after answering their question.

    Args:
        order: Display order number starting from 1. Use sequential numbers.
        actions_json: JSON array of action objects with label and optional url, action, icon fields.

    Returns:
        Confirmation that quick actions were rendered.
    """
    try:
        actions = json.loads(actions_json)
        add_segment({"type": "quick_actions", "actions": actions, "order": order})
        labels = [a.get("label", "?") for a in actions]
        return f"Quick actions rendered: {', '.join(labels)} at position {order}"
    except json.JSONDecodeError as e:
        return f"Error parsing actions_json: {e}. Please provide valid JSON."


# Maximum number of sources to show in the UI cards
MAX_UI_SOURCES = 4


@tool(parse_docstring=True)
def search_docs(query: str) -> str:
    """Search the Infomaniak documentation for relevant information.

    Call this FIRST to get context before building your response.

    Args:
        query: The search query (in English).

    Returns:
        Formatted search results with content from documentation.
    """
    retriever = get_retriever()
    documents = retriever.search(query, top_k=settings.RAG_TOP_K)

    if not documents:
        return "No relevant documentation found for this query."

    # Build sources for UI and results for LLM
    sources: list[dict[str, Any]] = []
    results = []
    seen_titles: set[str] = set()

    for i, doc in enumerate(documents):
        title = doc.metadata.get("title", "Untitled")
        source = doc.metadata.get("source", "")
        product = doc.metadata.get("product", "")
        content = doc.page_content
        score = doc.metadata.get("score")

        # Add to text results (all documents for LLM context)
        # Include ranking for LLM to understand relevance
        result = f"[{i + 1}] **{title}** ({product})\n{content}\nSource: {source}"
        results.append(result)

        # Build source document for UI (deduplicated by title, limited count)
        if len(sources) < MAX_UI_SOURCES and title not in seen_titles:
            seen_titles.add(title)
            # Strip markdown for clean snippet display
            clean_content = strip_markdown(content)
            snippet = clean_content[:150] + "..." if len(clean_content) > 150 else clean_content
            sources.append({
                "title": title,
                "product": product or "Infomaniak",
                "url": source,
                "snippet": snippet,
                "rank": i + 1,
            })

    # Add sources for end of response
    if sources:
        add_sources(sources)

    return "\n\n---\n\n".join(results)


@tool(parse_docstring=True)
def finish_response() -> str:
    """Signal that you have finished building the response.

    Call this when you have completed all text and UI components.
    This MUST be the last tool you call.

    Returns:
        Confirmation that the response is complete.
    """
    return "RESPONSE_COMPLETE"


# All tools for the prototype agent
ALL_TOOLS = [
    search_docs,
    render_text,
    render_steps,
    render_platform_availability,
    render_quick_actions,
    finish_response,
]
