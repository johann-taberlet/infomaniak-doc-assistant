"""LangChain tools for the RAG agent."""

import json
from functools import cache
from typing import Any

from langchain.tools import tool

from app.config import settings
from app.models.schemas import (
    PlatformAvailabilityComponent,
    PlatformStatus,
    QuickAction,
    QuickActionsComponent,
    SourceCardsComponent,
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


# Global storage for UI components to be emitted during streaming
# This is populated by tools and consumed by the SSE stream
_pending_ui_components: list[Any] = []


def get_pending_ui_components() -> list[Any]:
    """Get and clear pending UI components."""
    global _pending_ui_components
    components = _pending_ui_components.copy()
    _pending_ui_components = []
    return components


def add_ui_component(component: Any) -> None:
    """Add a UI component to be emitted."""
    global _pending_ui_components
    _pending_ui_components.append(component)


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

    # Build UI component for sources
    sources: list[SourceDocument] = []
    results = []

    for doc in documents:
        title = doc.metadata.get("title", "Untitled")
        source = doc.metadata.get("source", "")
        product = doc.metadata.get("product", "")
        content = doc.page_content
        score = doc.metadata.get("score")

        # Add to text results
        result = f"**{title}** ({product})\n{content}\nSource: {source}"
        results.append(result)

        # Build source document for UI
        snippet = content[:150] + "..." if len(content) > 150 else content
        sources.append(
            SourceDocument(
                title=title,
                product=product or "Infomaniak",
                url=source,
                snippet=snippet,
                relevance_score=score,
            )
        )

    # Add SourceCards UI component
    if sources:
        add_ui_component(SourceCardsComponent(sources=sources))

    return "\n\n---\n\n".join(results)


@tool(parse_docstring=True)
def render_steps(title: str, steps_json: str) -> str:
    """Render an interactive step-by-step guide for procedural instructions.

    Use this tool when explaining how to do something with multiple steps.
    The user will see an interactive checklist they can mark as complete.

    Args:
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
        add_ui_component(component)

        return f"Step guide '{title}' with {len(steps)} steps has been rendered."
    except (json.JSONDecodeError, TypeError) as e:
        return f"Error parsing steps: {e}. Please provide valid JSON."


@tool(parse_docstring=True)
def render_quick_actions(actions_json: str) -> str:
    """Render contextual quick action buttons after your response.

    Use this tool to provide helpful follow-up actions like opening documentation,
    contacting support, or deep links to specific features.

    Args:
        actions_json: JSON array of action objects. Each object needs a label field.
                     Optional fields are url, action (open_docs/contact_support/copy), icon.

    Returns:
        Confirmation that quick actions were rendered.
    """
    try:
        actions_data = json.loads(actions_json)
        actions = [QuickAction(**action) for action in actions_data]

        component = QuickActionsComponent(actions=actions)
        add_ui_component(component)

        return f"Quick actions rendered: {', '.join(a.label for a in actions)}"
    except (json.JSONDecodeError, TypeError) as e:
        return f"Error parsing actions: {e}. Please provide valid JSON."


@tool(parse_docstring=True)
def render_platform_availability(feature: str, platforms_json: str) -> str:
    """Render a visual grid showing feature availability across platforms.

    Use this tool when discussing platform-specific limitations or availability.
    Shows checkmarks, partial support, or unavailable status for each platform.

    Args:
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
        add_ui_component(component)

        return f"Platform availability for '{feature}' rendered across {len(platforms)} platforms."
    except (json.JSONDecodeError, TypeError) as e:
        return f"Error parsing platforms: {e}. Please provide valid JSON."


# List of all available tools for the agent
ALL_TOOLS = [
    search_docs,
    render_steps,
    render_quick_actions,
    render_platform_availability,
]
