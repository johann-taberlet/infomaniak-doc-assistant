# Embedding Models

## Modèles Recommandés

| Modèle | Dimensions | Usage |
|--------|------------|-------|
| nomic-embed-text | 768 | Recommandé - bon équilibre |
| mxbai-embed-large | 1024 | Meilleure qualité |
| all-minilm | 384 | Prototypage rapide |

## Configuration Ollama

```python
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434"
)

# Dimension: 768
vector = embeddings.embed_query("Mon texte")
vectors = embeddings.embed_documents(["Doc 1", "Doc 2"])
```

## Avec Qdrant

```python
from langchain_qdrant import QdrantVectorStore

vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name="docs",
    embedding=embeddings,
)
```
