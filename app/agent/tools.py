"""LangChain tools for the RAG agent."""

import json
from contextvars import ContextVar
from functools import cache
from typing import Any

from langchain.tools import tool

from app.config import settings
from app.models.schemas import (
    PlatformAvailabilityComponent,
    PlatformStatus,
    QuickAction,
    QuickActionsComponent,
    SourceDocument,
    Step,
    StepGuideComponent,
)
from app.rag.retriever import QdrantRetriever


@cache
def get_retriever() -> QdrantRetriever:
    """Get a cached QdrantRetriever instance.

    Uses functools.cache for lazy initialization and connection reuse.
    """
    return QdrantRetriever()


# Context variables for request-scoped storage
_segments_var: ContextVar[list[dict[str, Any]]] = ContextVar("segments", default=[])
_sources_var: ContextVar[list[dict[str, Any]]] = ContextVar("sources", default=[])
_language_var: ContextVar[str | None] = ContextVar("language", default=None)


def get_segments() -> list[dict[str, Any]]:
    """Get current segments list (creates new list if not set)."""
    try:
        return _segments_var.get()
    except LookupError:
        segments: list[dict[str, Any]] = []
        _segments_var.set(segments)
        return segments


def add_segment(segment: dict[str, Any]) -> None:
    """Add a segment to the current request."""
    segments = get_segments()
    segments.append(segment)


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


def set_response_language(language: str) -> None:
    """Set the language for the current response."""
    _language_var.set(language)


def get_response_language() -> str | None:
    """Get the language for the current response."""
    try:
        return _language_var.get()
    except LookupError:
        return None


def reset_context() -> None:
    """Reset all context variables for a new request."""
    _segments_var.set([])
    _sources_var.set([])
    _language_var.set(None)


def collect_all_segments() -> tuple[list[dict[str, Any]], list[dict[str, Any]], str | None]:
    """Collect all segments, sources, and language, then reset context.

    Returns:
        Tuple of (segments sorted by order, sources, language)
    """
    segments = get_segments()
    sources = get_sources()
    language = get_response_language()

    # Sort segments by order
    sorted_segments = sorted(segments, key=lambda s: s.get("order", 0))

    # Reset for next request
    reset_context()

    return sorted_segments, sources, language


# Maximum number of sources to show in the UI cards (top N most relevant)
MAX_UI_SOURCES = 4


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
            snippet = content[:150] + "..." if len(content) > 150 else content
            source_doc = SourceDocument(
                title=title,
                product=product or "Infomaniak",
                url=source,
                snippet=snippet,
                relevance_score=score,
            )
            add_source(source_doc.model_dump(by_alias=True))

    return "\n\n---\n\n".join(results)


@tool(parse_docstring=True)
def render_text(order: int, content: str) -> str:
    """Output a text segment to the user.

    Use this tool to output any text you want the user to see.
    Call this multiple times with different order numbers to build your response.

    Args:
        order: Display order number starting from 1.
        content: The markdown text to display.

    Returns:
        Confirmation that text was rendered.
    """
    add_segment({"type": "text", "content": content, "order": order})
    return f"Text rendered at position {order}"


@tool(parse_docstring=True)
def finish_response(language: str) -> str:
    """Signal completion and STOP. Call this as your FINAL action, then call no more tools.

    After calling this tool, your response is complete. Do NOT call any other tools.

    Args:
        language: The language code used in your response (e.g., 'en', 'fr', 'de').

    Returns:
        Completion signal indicating you should stop.
    """
    set_response_language(language)
    return "RESPONSE_COMPLETE. Your turn is finished. Do not call any more tools."


@tool(parse_docstring=True)
def render_steps(order: int, title: str, steps_json: str) -> str:
    """Render an interactive step-by-step guide for procedural instructions.

    Use this tool when explaining how to do something with multiple steps.
    The user will see an interactive checklist they can mark as complete.

    Args:
        order: Display order number for this component.
        title: The title of the guide, like How to share a folder on kDrive.
        steps_json: JSON array of step objects. Each object needs number, title,
                   description fields. Optional fields are details and command.

    Returns:
        Confirmation that the step guide was rendered.
    """
    try:
        steps_data = json.loads(steps_json)
        steps = [Step(**step) for step in steps_data]

        component = StepGuideComponent(title=title, steps=steps)
        segment = component.model_dump(by_alias=True)
        segment["order"] = order
        add_segment(segment)

        return f"Step guide '{title}' with {len(steps)} steps rendered at position {order}."
    except (json.JSONDecodeError, TypeError) as e:
        return f"Error parsing steps: {e}. Please provide valid JSON."


@tool(parse_docstring=True)
def render_quick_actions(order: int, actions_json: str) -> str:
    """Render contextual quick action buttons after your response.

    Use this tool to provide helpful follow-up actions like opening documentation,
    contacting support, or deep links to specific features.

    Args:
        order: Display order number for this component.
        actions_json: JSON array of action objects. Each object needs a label field.
                     Optional fields are url, action (open_docs/contact_support/copy), icon.

    Returns:
        Confirmation that quick actions were rendered.
    """
    try:
        actions_data = json.loads(actions_json)
        actions = [QuickAction(**action) for action in actions_data]

        component = QuickActionsComponent(actions=actions)
        segment = component.model_dump(by_alias=True)
        segment["order"] = order
        add_segment(segment)

        return f"Quick actions rendered at position {order}: {', '.join(a.label for a in actions)}"
    except (json.JSONDecodeError, TypeError) as e:
        return f"Error parsing actions: {e}. Please provide valid JSON."


@tool(parse_docstring=True)
def render_platform_availability(order: int, feature: str, platforms_json: str) -> str:
    """Render a visual grid showing feature availability across platforms.

    Use this tool when discussing platform-specific limitations or availability.
    Shows checkmarks, partial support, or unavailable status for each platform.

    Args:
        order: Display order number for this component.
        feature: The feature name like Lite Sync or Screen sharing.
        platforms_json: JSON array of platform status objects. Each needs platform
                       (web/windows/macos/ios/android/linux) and availability (full/partial/none).
                       Optional notes field for additional context.

    Returns:
        Confirmation that platform availability was rendered.
    """
    try:
        platforms_data = json.loads(platforms_json)
        platforms = [PlatformStatus(**p) for p in platforms_data]

        component = PlatformAvailabilityComponent(feature=feature, platforms=platforms)
        segment = component.model_dump(by_alias=True)
        segment["order"] = order
        add_segment(segment)

        return f"Platform availability for '{feature}' rendered at position {order}."
    except (json.JSONDecodeError, TypeError) as e:
        return f"Error parsing platforms: {e}. Please provide valid JSON."


# List of all available tools for the agent
ALL_TOOLS = [
    search_docs,
    render_text,
    render_steps,
    render_quick_actions,
    render_platform_availability,
    finish_response,
]
