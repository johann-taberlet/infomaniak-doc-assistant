# Langfuse Observability

## Configuration

```python
# Via environment variables
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Intégration LangChain

```python
from langfuse.callback import CallbackHandler

langfuse_handler = CallbackHandler()

response = chain.invoke(
    {"input": "Question"},
    config={"callbacks": [langfuse_handler]}
)
```

## Décorateur @observe()

```python
from langfuse import observe

@observe()
def my_function(input):
    # Automatiquement tracé
    return llm.invoke(input)
```

## Désactivation Conditionnelle

```python
def get_langfuse_handler():
    if not settings.LANGFUSE_ENABLED:
        return None
    return CallbackHandler(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
    )
```

## Métriques Capturées

- Tokens (input, output, total)
- Latence par span
- Inputs/Outputs complets
- Coût (calculé automatiquement)
