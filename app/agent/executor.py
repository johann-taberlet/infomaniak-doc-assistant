"""Agent executor for the Infomaniak documentation assistant."""

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import ALL_TOOLS
from app.llm import get_chat_model


# Memory checkpoint for conversation persistence
_checkpointer = InMemorySaver()


def get_agent():
    """Create and return a ReAct agent for the documentation assistant.

    Returns:
        A LangGraph ReAct agent with search and UI rendering tools, plus conversation memory.
    """
    model = get_chat_model()

    agent = create_react_agent(
        model=model,
        tools=ALL_TOOLS,
        checkpointer=_checkpointer,
        prompt=SYSTEM_PROMPT,
    )

    return agent
