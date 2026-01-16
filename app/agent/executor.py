"""Agent executor for the Infomaniak documentation assistant."""

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import search_docs
from app.llm import get_chat_model


# Memory checkpoint for conversation persistence
_checkpointer = InMemorySaver()


def get_agent():
    """Create and return a ReAct agent for the documentation assistant.

    Returns:
        A LangGraph ReAct agent with search_docs tool and conversation memory.
    """
    model = get_chat_model()
    tools = [search_docs]

    agent = create_react_agent(
        model=model,
        tools=tools,
        checkpointer=_checkpointer,
        prompt=SYSTEM_PROMPT,
    )

    return agent
