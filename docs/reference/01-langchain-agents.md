# LangChain Agent Orchestration

## Imports Nécessaires

```python
from langchain.agents import create_agent, AgentExecutor
from langchain.tools import tool, ToolRuntime
from langchain.memory import ConversationBufferMemory
from langchain.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig, RunnablePassthrough, chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import InjectedState, create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.types import Command
from typing import Annotated
```

## Création d'Agents avec Tools

```python
@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(model, tools=[search])
```

## Agent avec Docstrings Parsées

```python
@tool(parse_docstring=True)
def search_docs(query: str) -> str:
    """Search documentation for relevant information.
    Args:
        query: The search query
    """
    return retriever.invoke(query)

model = ChatOllama(model="qwen3:8b")
agent = create_agent(model, [search_docs], checkpointer=InMemorySaver())
```

## Agent Executor Configuration

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)
```

## LCEL (LangChain Expression Language)

```python
prompt = ChatPromptTemplate([
    ("system", "You are a helpful assistant."),
    ("human", "{user_input}"),
    ("placeholder", "{messages}"),
])

model_with_tools = model.bind_tools([search_tool], tool_choice=search_tool.name)
model_chain = prompt | model_with_tools

@chain
def tool_chain(user_input: str, config: RunnableConfig):
    input_ = {"user_input": user_input}
    ai_msg = model_chain.invoke(input_, config=config)
    tool_msgs = search_tool.batch(ai_msg.tool_calls, config=config)
    return model_chain.invoke({**input_, "messages": [ai_msg, *tool_msgs]}, config=config)
```

## RAG Chain avec LCEL

```python
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

## ReAct Agent avec create_react_agent

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=ChatOllama(model="qwen3:8b"),
    tools=[search_docs],
    checkpointer=InMemorySaver()
)

# Invoke with thread_id for memory
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Question"}]},
    {"configurable": {"thread_id": "session-123"}}
)
```

## Best Practices

- Utiliser `@tool(parse_docstring=True)` avec docstrings complètes
- Préférer LangGraph `create_react_agent` à AgentExecutor pour les nouveaux projets
- Utiliser `InMemorySaver` comme checkpointer pour la mémoire
- Stop tokens: `.bind(stop=["\nObservation"])` pour ReAct

## Résumé

| Concept | Description |
|---------|-------------|
| `@tool` decorator | Définit des tools réutilisables |
| `create_react_agent()` | Crée un agent ReAct avec tools |
| `InMemorySaver` | Checkpointer pour mémoire de conversation |
| `bind_tools()` | Lie des tools à un modèle |
| LCEL (`\|` operator) | Chaînage de composants |
