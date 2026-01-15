# Qdrant Vector Database

## Client Python

```python
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")
```

## Création de Collection

```python
client.create_collection(
    collection_name="infomaniak_docs",
    vectors_config=models.VectorParams(
        size=768,  # Dimension des embeddings (nomic-embed-text)
        distance=models.Distance.COSINE,
    ),
)
```

## Upsert de Documents

```python
client.upsert(
    collection_name="infomaniak_docs",
    points=[
        models.PointStruct(
            id=1,
            vector=[0.1, 0.2, ...],  # 768 dimensions
            payload={
                "source": "docs.infomaniak.com",
                "title": "Partage de fichiers",
                "content": "Le texte du chunk...",
            }
        ),
    ]
)
```

## Recherche avec Filtres

```python
results = client.search(
    collection_name="infomaniak_docs",
    query_vector=query_embedding,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="language",
                match=models.MatchValue(value="fr")
            )
        ]
    ),
    limit=5,
    with_payload=True
)
```

## Recherche Alternative (query_points)

```python
results = client.query_points(
    collection_name="infomaniak_docs",
    query=query_vector,
    limit=5,
    with_payload=True,
)
```

## Intégration LangChain

```python
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings

vector_store = QdrantVectorStore(
    client=client,
    collection_name="infomaniak_docs",
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
```

## Docker

```bash
docker run -d -p 6333:6333 -v qdrant_data:/qdrant/storage qdrant/qdrant
```

## Health Check

```bash
curl http://localhost:6333/healthz
curl http://localhost:6333/collections
```
