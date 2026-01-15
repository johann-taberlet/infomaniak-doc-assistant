# Ollama LLM Serving

## Installation

```bash
brew install ollama  # macOS
ollama serve

# Télécharger les modèles
ollama pull qwen3:8b
ollama pull nomic-embed-text
```

## Modèles Recommandés

| Usage | Modèle | VRAM |
|-------|--------|------|
| Embeddings | nomic-embed-text | 1-2 GB |
| Chat | qwen3:8b | 8-12 GB |

## ChatOllama avec LangChain

```python
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOllama(
    model="qwen3:8b",
    base_url="http://localhost:11434",
    temperature=0.7,
    num_ctx=4096,
)

messages = [
    SystemMessage(content="Tu es un assistant."),
    HumanMessage(content="Bonjour")
]

response = llm.invoke(messages)
```

## Streaming

```python
for chunk in llm.stream(messages):
    print(chunk.content, end="", flush=True)
```

## Embeddings Ollama

```python
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434"
)

# Dimension: 1024
vector = embeddings.embed_query("Mon texte")
doc_vectors = embeddings.embed_documents(["Doc 1", "Doc 2"])
```

## Configuration Optimisée

```python
llm = ChatOllama(
    model="qwen3:8b",
    num_ctx=4096,
    temperature=0.7,
    top_p=0.9,
    keep_alive="5m",
)
```

## Commandes Utiles

```bash
ollama list    # Modèles installés
ollama ps      # Modèles en mémoire
ollama stop    # Arrêter un modèle
```
