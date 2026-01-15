# RAG Pipeline Architecture

## Chunking Récursif (Recommandé)

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["##", "###", "\n\n", "\n", ". ", " "]
)
chunks = text_splitter.split_text(text)
```

## Tailles de Chunks Optimales

| Type de Document | Taille (tokens) | Overlap |
|------------------|-----------------|---------|
| FAQ/Support | 200-400 | 10-15% |
| Documentation Technique | 600-1200 | 20-25% |
| News/Blog | 400-600 | 15-20% |

**Recommandation**: 500 tokens avec 10% overlap (50 tokens).

## Métadonnées à Conserver

- Section/Header (critique)
- Source URL/Path
- Document type

## Recherche Hybride (BM25 + Dense)

```python
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

bm25_retriever = BM25Retriever.from_documents(documents)
dense_retriever = vectorstore.as_retriever()

hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, dense_retriever],
    weights=[0.5, 0.5]
)
```

## Query Expansion

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)
```

## RAG Chain avec Sources

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

## Métriques RAG

| Métrique | Description |
|----------|-------------|
| Context Precision | % docs récupérés pertinents |
| Context Recall | % docs pertinents récupérés |
| Faithfulness | Réponse supportée par contexte |
