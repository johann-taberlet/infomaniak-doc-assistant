# Conversation Memory

## InMemorySaver (Développement)

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=checkpointer
)

# Utiliser avec thread_id pour isoler les conversations
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Bonjour"}]},
    {"configurable": {"thread_id": "session-123"}}
)
```

## Persistance avec thread_id

```python
# Même thread_id = même conversation
config = {"configurable": {"thread_id": "user-session-abc"}}

# Premier message
agent.invoke({"messages": ["Je m'appelle Jean"]}, config)

# Deuxième message - se souvient du nom
agent.invoke({"messages": ["Comment je m'appelle?"]}, config)
```

## Options de Checkpointer

| Checkpointer | Usage |
|--------------|-------|
| `InMemorySaver` | Développement/Tests |
| `PostgresSaver` | Production (sync) |
| `AsyncRedisSaver` | Production (async) |
