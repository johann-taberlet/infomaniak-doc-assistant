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
from app.observability.langfuse import get_langfuse_handler

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

    # Detect if message is likely English (simple heuristic)
    english_indicators = ['what', 'how', 'why', 'when', 'where', 'which', 'can', 'do', 'does', 'is', 'are', 'the', 'and', 'to', 'in', 'on', 'for']
    message_lower = message.lower()
    english_word_count = sum(1 for word in english_indicators if word in message_lower.split())
    is_likely_english = english_word_count >= 2

    # Add explicit language instruction with the user message
    if is_likely_english:
        user_content = f"[RESPOND IN ENGLISH - The user wrote in English]\n\n{message}"
    else:
        user_content = message

    # Build messages: system + history + current message
    messages: list[BaseMessage] = [
        SystemMessage(content=system_prompt),
        *history,
        HumanMessage(content=user_content),
    ]

    # Add user message to history
    add_to_conversation(session_id, HumanMessage(content=message))

    # Accumulate response for history
    full_response = ""

    # Get optional Langfuse handler for observability
    langfuse_handler = get_langfuse_handler()
    config = {"callbacks": [langfuse_handler]} if langfuse_handler else None

    async for chunk in model.astream(messages, config=config):
        if chunk.content:
            content = str(chunk.content)
            full_response += content
            yield content

    # Add assistant response to history
    add_to_conversation(session_id, AIMessage(content=full_response))
