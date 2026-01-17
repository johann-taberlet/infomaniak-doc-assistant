"""Agent executor for the Infomaniak documentation assistant."""

from langgraph.prebuilt import create_react_agent

from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import ALL_TOOLS
from app.llm import get_chat_model


def get_agent():
    """Create and return a ReAct agent for the documentation assistant.

    Returns:
        A LangGraph ReAct agent with search and UI rendering tools.

    Note:
        Conversation memory is disabled because it causes infinite loops.
        The LLM sees previous tool calls in history and keeps calling more tools.
        Each request is handled independently for now.
    """
    model = get_chat_model()

    agent = create_react_agent(
        model=model,
        tools=ALL_TOOLS,
        prompt=SYSTEM_PROMPT,
        # No checkpointer - each request is independent
        # TODO: Implement custom memory that only keeps user messages and final responses
    )

    return agent
