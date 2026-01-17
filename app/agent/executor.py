"""Agent executor for the Infomaniak documentation assistant.

Implements simplified NDJSON streaming:
1. Search documentation for relevant information
2. Stream NDJSON response from LLM for progressive UI rendering
"""

from collections.abc import AsyncGenerator

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from app.agent.prompts import NDJSON_SYSTEM_PROMPT
from app.agent.tools import search_docs
from app.llm import get_chat_model

# In-memory conversation store (session_id -> messages)
_conversations: dict[str, list[BaseMessage]] = {}


def get_conversation_history(session_id: str) -> list[BaseMessage]:
    """Retrieve conversation history for a session."""
    return _conversations.get(session_id, [])


def add_to_conversation(session_id: str, message: BaseMessage) -> None:
    """Add a message to the conversation history."""
    if session_id not in _conversations:
        _conversations[session_id] = []
    _conversations[session_id].append(message)
    # Keep only last 10 messages to prevent context overflow
    if len(_conversations[session_id]) > 10:
        _conversations[session_id] = _conversations[session_id][-10:]


def clear_conversation(session_id: str) -> None:
    """Clear conversation history for a session."""
    if session_id in _conversations:
        del _conversations[session_id]


async def search_documentation(query: str) -> str:
    """Execute RAG search and return context.

    Args:
        query: The user's question to search for.

    Returns:
        Formatted search results with content and source citations.
    """
    return search_docs.invoke({"query": query})


async def stream_ndjson_response(
    message: str,
    search_context: str,
    session_id: str,
) -> AsyncGenerator[str, None]:
    """Stream NDJSON response from LLM.

    Args:
        message: The user's question.
        search_context: Documentation context from RAG search.
        session_id: Session ID for conversation memory.

    Yields:
        String chunks of NDJSON content as they are generated.
    """
    model = get_chat_model()

    # Build system prompt with search context
    system_prompt = NDJSON_SYSTEM_PROMPT.format(context=search_context)

    # Get conversation history
    history = get_conversation_history(session_id)

    # Build messages: system + history + current message
    messages: list[BaseMessage] = [
        SystemMessage(content=system_prompt),
        *history,
        HumanMessage(content=message),
    ]

    # Add user message to history
    add_to_conversation(session_id, HumanMessage(content=message))

    # Accumulate response for history
    full_response = ""

    async for chunk in model.astream(messages):
        if chunk.content:
            content = str(chunk.content)
            full_response += content
            yield content

    # Add assistant response to history
    add_to_conversation(session_id, AIMessage(content=full_response))
