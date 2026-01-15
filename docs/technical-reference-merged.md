# Documentation Technique Complète - Infomaniak Doc Assistant

**Date:** 15 Janvier 2026
**Version:** 2.0 (Fusionnée)
**Auteur:** Johann Taberlet

---

## Table des Matières

1. [LangChain Agent Orchestration](#1-langchain-agent-orchestration)
2. [RAG Pipeline Architecture](#2-rag-pipeline-architecture)
3. [Qdrant Vector Database](#3-qdrant-vector-database)
4. [Ollama LLM Serving](#4-ollama-llm-serving)
5. [Pydantic Validation](#5-pydantic-validation)
6. [FastAPI Async & Streaming](#6-fastapi-async--streaming)
7. [Langfuse Observability](#7-langfuse-observability)
8. [Embedding Models](#8-embedding-models)
9. [Conversation Memory](#9-conversation-memory)
10. [Docker Deployment](#10-docker-deployment)
11. [Semantic Chunking](#11-semantic-chunking)
12. [Error Handling & Resilience](#12-error-handling--resilience)
13. [Web Scraping Documentation](#13-web-scraping-documentation)

---

## 1. LangChain Agent Orchestration

### 1.1 Imports Nécessaires

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

### 1.2 Création d'Agents avec Tools Personnalisés

```python
@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

agent = create_agent(model, tools=[search, get_weather])
```

### 1.3 Agent avec Docstrings Parsées

```python
@tool(parse_docstring=True)
def search_docs(query: str) -> str:
    """Search documentation for relevant information.
    Args:
        query: The search query
    """
    return retriever.invoke(query)

model = ChatOllama(model="qwen2.5:7b")
agent = create_agent(model, [search_docs], checkpointer=InMemorySaver())
```

### 1.4 Agent Executor Configuration

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)
```

### 1.5 LCEL (LangChain Expression Language)

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

### 1.6 RAG Chain avec LCEL

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

### 1.7 ReAct Agent avec Custom State

```python
class CustomState(AgentState):
    user_name: str

def greet(state: Annotated[CustomState, InjectedState]) -> str:
    """Use this to greet the user by name."""
    user_name = state["user_name"]
    return f"Hello {user_name}!"

agent = create_react_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[greet],
    state_schema=CustomState
)
```

### 1.8 ToolRuntime pour Accès au State

```python
class CustomState(AgentState):
    user_name: str

@tool
def update_user_info(runtime: ToolRuntime[CustomContext, CustomState]) -> Command:
    """Look up and update user info."""
    user_id = runtime.context.user_id
    name = "John Smith" if user_id == "user_123" else "Unknown user"
    return Command(update={
        "user_name": name,
        "messages": [
            ToolMessage(
                "Successfully looked up user information",
                tool_call_id=runtime.tool_call_id
            )
        ]
    })

agent = create_agent(
    model="gpt-5-nano",
    tools=[update_user_info],
    state_schema=CustomState,
    context_schema=CustomContext,
)
```

### 1.9 Best Practices

- Utiliser `@tool(parse_docstring=True)` avec docstrings complètes
- Préférer LangGraph à AgentExecutor pour les nouveaux projets
- Utiliser `InMemorySaver` comme checkpointer pour la mémoire
- Stop tokens: `.bind(stop=["\nObservation"])` pour ReAct

### Résumé des Concepts Clés

| Concept | Description |
|---------|-------------|
| `@tool` decorator | Définit des tools réutilisables |
| `create_agent()` | Crée un agent avec modèle et tools |
| `AgentExecutor` | Gère l'exécution itérative |
| `create_react_agent()` | Agent ReAct avec raisonnement explicite |
| `bind_tools()` | Lie des tools à un modèle |
| `ToolRuntime` | Accès au contexte et state depuis un tool |
| `Command(update={})` | Met à jour le state depuis un tool |
| LCEL (`|` operator) | Chaînage de composants |

---

## 2. RAG Pipeline Architecture

### 2.1 Stratégies de Chunking

#### Chunking Récursif (Recommandé comme baseline)

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = text_splitter.split_text(text)
```

#### Configuration Optimisée pour Documentation

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["##", "###", "\n\n", "\n", ". ", " "],
)
```

#### Chunking Sémantique

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

text_splitter = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",  # ou 'standard_deviation', 'interquartile', 'gradient'
    breakpoint_threshold_amount=95.0
)
docs = text_splitter.create_documents([your_text])
```

### 2.2 Tailles de Chunks Optimales

| Type de Document | Taille (tokens) | Overlap |
|------------------|-----------------|---------|
| FAQ/Support | 200-400 | 10-15% |
| Documentation Technique | 600-1200 | 20-25% |
| Articles Académiques | 1000-2000 | 30%+ |
| Documents Juridiques | 800-1500 | 25-30% |
| News/Blog | 400-600 | 15-20% |

**Recommandation baseline**: 400-800 tokens avec 20% overlap.
**Recommandation 2025**: 512 tokens avec 10-15% overlap (50-75 tokens).

### 2.3 Métadonnées à Conserver

- Section/Header (critique)
- Source URL/Path
- Document type
- Page number (PDF)

### 2.4 Recherche Hybride (BM25 + Dense)

```python
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

# BM25 pour les correspondances exactes
bm25_retriever = BM25Retriever.from_documents(documents)

# Dense pour la compréhension sémantique
dense_retriever = vectorstore.as_retriever()

# Fusion via Reciprocal Rank Fusion (RRF)
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, dense_retriever],
    weights=[0.5, 0.5]
)
```

**Amélioration**: 10-20% vs approche unique.

### 2.5 Reranking avec Cross-Encoders

```python
from sentence_transformers import CrossEncoder

cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")

# Score chaque paire query-document
pairs = [[query, doc.page_content] for doc in initial_results]
scores = cross_encoder.predict(pairs)

# Trier par score de pertinence
reranked = sorted(zip(scores, initial_results), reverse=True)
```

**Amélioration**: 15-25% sur la qualité des réponses.

### 2.6 Query Expansion

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

# Génère 3-5 reformulations de la query
retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)
```

**Améliore le recall de 20-35%**.

### 2.7 RAG Chain avec Sources

```python
from langchain_classic.chains import create_retrieval_chain

rag_chain = create_retrieval_chain(retriever, question_answer_chain)
# result["source_documents"] contient les sources
```

### 2.8 Métriques d'Évaluation RAG

| Métrique | Description |
|----------|-------------|
| **Context Precision** | % des docs récupérés qui sont pertinents |
| **Context Recall** | % des docs pertinents effectivement récupérés |
| **Answer Relevancy** | La réponse adresse-t-elle la question ? |
| **Faithfulness** | La réponse est-elle supportée par le contexte ? |

```python
from ragas import evaluate
from ragas.metrics import context_precision, context_recall, faithfulness

results = evaluate(
    dataset=eval_dataset,
    metrics=[context_precision, context_recall, faithfulness]
)

# Score RAG global composite
overall_score = (
    context_precision * 0.2 +
    context_recall * 0.2 +
    answer_relevancy * 0.3 +
    faithfulness * 0.3
)
```

### 2.9 Semantic vs Fixed-Size Chunking

- **Semantic chunking**: +9% recall, plus lent, plus coûteux
- **Fixed-size**: Rapide, baseline solide

---

## 3. Qdrant Vector Database

### 3.1 Client Python

```python
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")
```

### 3.2 Création de Collections

```python
# Collection avec stockage sur disque
client.create_collection(
    collection_name="infomaniak_docs",
    vectors_config=models.VectorParams(
        size=1024,  # Dimension des embeddings
        distance=models.Distance.COSINE,
        on_disk=True
    ),
    hnsw_config=models.HnswConfigDiff(on_disk=True),
)
```

### 3.3 Configuration HNSW et Quantization

```python
# Mise à jour des paramètres à runtime
client.update_collection(
    collection_name="infomaniak_docs",
    hnsw_config=models.HnswConfigDiff(
        m=32,           # Nombre de voisins pour le graphe HNSW
        ef_construct=123  # Taille liste dynamique pendant construction
    ),
    quantization_config=models.ScalarQuantization(
        scalar=models.ScalarQuantizationConfig(
            type=models.ScalarType.INT8,
            quantile=0.8,
            always_ram=False
        )
    )
)
```

### 3.4 Opérations Batch (Upsert)

```python
client.upsert(
    collection_name="infomaniak_docs",
    points=[
        models.PointStruct(
            id=1,
            vector=[0.1, 0.2, ...],  # 1024 dimensions
            payload={
                "source": "docs.infomaniak.com",
                "page": "/kdrive/sharing",
                "title": "Partage de fichiers",
                "language": "fr",
                "section": "sharing"
            }
        ),
        # ... autres points
    ]
)
```

### 3.5 Recherche avec Filtres

```python
results = client.search(
    collection_name="infomaniak_docs",
    query_vector=[0.2, 0.1, 0.9, ...],
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="language",
                match=models.MatchValue(value="fr")
            )
        ],
        must_not=[
            models.FieldCondition(
                key="deprecated",
                match=models.MatchValue(value=True)
            )
        ]
    ),
    limit=5,
    with_payload=True
)
```

### 3.6 Recherche Alternative (query_points)

```python
results = client.query_points(
    collection_name="docs",
    query=query_vector,
    query_filter=models.Filter(
        must=[models.FieldCondition(key="product", match=models.MatchValue(value="kdrive"))]
    ),
    limit=5,
    with_payload=True,
)
```

### 3.7 Condition Range

```python
models.FieldCondition(
    key="price",
    range=models.Range(
        gte=100.0,
        lte=450.0,
    ),
)
```

### 3.8 Index de Payload

```python
# Index texte avec phrase matching
client.create_payload_index(
    collection_name="infomaniak_docs",
    field_name="title",
    field_schema=models.TextIndexParams(
        type=models.TextIndexType.TEXT,
        tokenizer=models.TokenizerType.WORD,
        lowercase=True,
        phrase_matching=True,
    ),
)

# Index entier pour filtres range
client.create_payload_index(
    collection_name="infomaniak_docs",
    field_name="page_number",
    field_schema=models.IntegerIndexParams(
        type=models.IntegerIndexType.INTEGER,
        lookup=False,
        range=True,
    ),
)
```

### 3.9 Intégration LangChain

```python
from langchain_qdrant import QdrantVectorStore

vector_store = QdrantVectorStore(
    client=client,
    collection_name="docs",
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
```

### 3.10 Docker

```yaml
qdrant:
  image: qdrant/qdrant:latest
  ports:
    - "6333:6333"
    - "6334:6334"
  volumes:
    - qdrant_storage:/qdrant/storage
```

---

## 4. Ollama LLM Serving

### 4.1 Installation et Configuration

```bash
# Installation
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve

# Téléchargement des modèles
ollama pull qwen2.5:7b
ollama pull mistral:v0.3
ollama pull nomic-embed-text

# Vérifier les modèles
ollama list
ollama ps

# Quantification pour moins de VRAM
ollama pull qwen2.5:7b-q4_K_M
```

### 4.2 Exigences Matérielles

| Taille du modèle | RAM Minimum | RAM Recommandée |
|------------------|-------------|-----------------|
| 1B-3B | 4 GB | 8 GB |
| 7B | 8 GB | 16 GB |
| 13B-14B | 16 GB | 32 GB |
| 30B+ | 32 GB | 64 GB+ |

### 4.3 Modèles Recommandés

| Usage | Modèle | VRAM |
|-------|--------|------|
| Embeddings | nomic-embed-text | 1-2 GB |
| Chat (qualité) | qwen2.5:7b | 8-12 GB |
| Chat (vitesse) | mistral:7b | 8-10 GB |

### 4.4 Intégration LangChain avec ChatOllama

```python
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOllama(
    model="qwen2.5:7b",
    base_url="http://localhost:11434",
    temperature=0.7,
    num_ctx=4096,
    num_gpu=40,
    keep_alive="10m",
    validate_model_on_init=True
)

messages = [
    SystemMessage(content="Tu es un assistant technique expert."),
    HumanMessage(content="Explique les décorateurs Python.")
]

# Invocation simple
response = llm.invoke(messages)

# Streaming
for chunk in llm.stream(messages):
    print(chunk.content, end="", flush=True)
```

### 4.5 Embeddings Ollama

```python
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434"
)

# Générer des embeddings
vector = embeddings.embed_query("LangChain est un framework IA")
print(f"Dimension: {len(vector)}")  # 1024

# Usage avec documents
query_vec = embeddings.embed_query("Ma question")
doc_vecs = embeddings.embed_documents(["Doc 1", "Doc 2"])

# Avec ChromaDB
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
```

### 4.6 Configuration Optimisée

```python
llm = ChatOllama(
    model="qwen2.5:7b",

    # Paramètres de performance
    num_ctx=4096,
    num_batch=512,
    num_thread=8,
    num_gpu=40,

    # Paramètres de génération
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    repeat_penalty=1.1,
    num_predict=512,
    timeout=60,

    # Gestion mémoire
    keep_alive="5m",
)
```

### 4.7 Variables d'Environnement

```bash
export OLLAMA_NUM_GPU=40
export OLLAMA_GPU_OVERHEAD=0
export OLLAMA_MAX_LOADED_MODELS=2
export OLLAMA_MAX_QUEUE=512
export OLLAMA_NUM_PARALLEL=4
```

### 4.8 Gestion d'Erreurs

```python
try:
    llm = ChatOllama(model="qwen2.5:7b")
    llm.invoke("test")
except Exception as e:
    if "not found" in str(e).lower():
        print("Exécutez: ollama pull qwen2.5:7b")
```

---

## 5. Pydantic Validation

### 5.1 Modèles de Base

```python
from pydantic import BaseModel, Field, ValidationError, ConfigDict

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    session_id: str | None = None
    language: str = "fr"

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0.0, le=1.0)

# Validation
try:
    request = ChatRequest(message="Comment partager un dossier?")
except ValidationError as e:
    print(e.errors())
```

### 5.2 Modèle pour Réponse LLM

```python
class LLMResponse(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    answer: str = Field(..., min_length=1, description="Réponse principale")
    sources: list[str] = Field(default_factory=list, description="Sources citées")
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
```

### 5.3 Field Validator

```python
from pydantic import BaseModel, field_validator, ValidationInfo
import re

class UserQuery(BaseModel):
    query: str
    max_tokens: int = 1000

    @field_validator('query')
    @classmethod
    def query_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()

    @field_validator('max_tokens')
    @classmethod
    def validate_tokens(cls, v: int) -> int:
        if not 100 <= v <= 4000:
            raise ValueError('max_tokens must be between 100 and 4000')
        return v
```

### 5.4 Model Validator (Cross-field)

```python
from pydantic import BaseModel, model_validator
from typing import Any

class DateRange(BaseModel):
    start_date: str
    end_date: str

    @model_validator(mode='after')
    def check_dates_order(self) -> 'DateRange':
        if self.start_date > self.end_date:
            raise ValueError('start_date must be before end_date')
        return self
```

### 5.5 Wrap Validator pour Logging

```python
from pydantic import BaseModel, model_validator, ModelWrapValidatorHandler, ValidationError
import logging

class UserModel(BaseModel):
    username: str

    @model_validator(mode='wrap')
    @classmethod
    def log_failed_validation(cls, data: Any, handler: ModelWrapValidatorHandler) -> 'UserModel':
        try:
            return handler(data)
        except ValidationError:
            logging.error('Model %s failed to validate with data %s', cls, data)
            raise
```

### 5.6 Validation JSON et Génération Schema

```python
# Validation JSON
try:
    response = LLMResponse.model_validate_json(raw_json)
except ValidationError as e:
    for error in e.errors():
        print(f"Erreur: {error['loc']} - {error['msg']}")

# Génération Schema pour Prompt
schema = LLMResponse.model_json_schema()
prompt = f"Réponds en JSON valide selon ce schema:\n{json.dumps(schema, indent=2)}"
```

### 5.7 Méthodes Principales

| Méthode | Description |
|---------|-------------|
| `Model.model_validate(data)` | Valide un dict et retourne une instance |
| `model.model_dump()` | Sérialise en dictionnaire |
| `model.model_dump(by_alias=True)` | Sérialise avec les aliases |
| `model.model_dump_json()` | Sérialise en JSON string |
| `Model.model_json_schema()` | Génère le JSON Schema |
| `Model.model_validate_json(json_str)` | Valide depuis JSON string |

---

## 6. FastAPI Async & Streaming

### 6.1 Application de Base

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.post("/chat")
async def chat(request: ChatRequest):
    response = await chain.ainvoke({"question": request.message})
    return {"response": response}
```

### 6.2 Lifespan Events

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.llm = ChatOllama(model="qwen2.5:7b")
    yield
    # Shutdown

app = FastAPI(lifespan=lifespan)
```

### 6.3 CORS Middleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6.4 StreamingResponse avec Async Generator

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

async def token_generator():
    for i in range(100):
        yield f"token_{i} "
        await asyncio.sleep(0.1)

@app.get("/stream")
async def stream_tokens():
    return StreamingResponse(
        token_generator(),
        media_type="text/plain"
    )
```

### 6.5 Server-Sent Events (SSE)

```python
import json

def format_sse_event(data: dict, event_type: str = "message") -> str:
    lines = [f"event: {event_type}"]
    lines.append(f"data: {json.dumps(data)}")
    return "\n".join(lines) + "\n\n"

async def sse_stream(request: Request, prompt: str):
    try:
        async for token in generate_tokens(prompt):
            if await request.is_disconnected():
                break
            yield format_sse_event({"token": token}, "chunk")

        yield format_sse_event({"status": "complete"}, "done")
    except Exception as e:
        yield format_sse_event({"error": str(e)}, "error")

@app.post("/chat/stream")
async def chat_stream(request: Request, prompt: str):
    return StreamingResponse(
        sse_stream(request, prompt),
        media_type="text/event-stream"
    )
```

### 6.6 SSE Streaming Simplifié

```python
async def stream_generator():
    async for chunk in chain.astream({"question": query}):
        yield f"data: {chunk}\n\n"

@app.get("/stream")
async def stream():
    return StreamingResponse(stream_generator(), media_type="text/event-stream")
```

### 6.7 BackgroundTasks

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(write_log, f"Notification sent to {email}\n")
    return {"message": "Notification sent in the background"}
```

### 6.8 Timeout Management

```python
import asyncio

async def timeout_aware_stream(
    request: Request,
    prompt: str,
    timeout_seconds: float = 30.0
):
    start_time = asyncio.get_event_loop().time()

    async for token in generate_tokens(prompt):
        elapsed = asyncio.get_event_loop().time() - start_time
        if elapsed > timeout_seconds:
            yield "[TIMEOUT: Generation exceeded maximum duration]\n"
            break

        if await request.is_disconnected():
            break

        yield token
```

### 6.9 Exception Handlers

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

### 6.10 LangChain Streaming Callback

```python
from langchain.callbacks.base import AsyncCallbackHandler
import asyncio

class StreamingCallbackHandler(AsyncCallbackHandler):
    def __init__(self):
        self.queue: asyncio.Queue[str] = asyncio.Queue()
        self.done = asyncio.Event()

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        if token:
            await self.queue.put(token)

    async def on_llm_end(self, response, **kwargs) -> None:
        self.done.set()

    async def aiter_tokens(self):
        while not self.done.is_set() or not self.queue.empty():
            try:
                token = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                yield token
            except asyncio.TimeoutError:
                if self.done.is_set():
                    break
```

---

## 7. Langfuse Observability

### 7.1 Configuration

```python
import os

os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_BASE_URL"] = "https://cloud.langfuse.com"
```

### 7.2 Intégration LangChain avec CallbackHandler

```python
from langfuse.callback import CallbackHandler
from langchain_openai import ChatOpenAI

langfuse_handler = CallbackHandler(
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
)

llm = ChatOpenAI(model="gpt-4")
chain = prompt | llm

response = chain.invoke(
    {"input": "What is LLM observability?"},
    config={"callbacks": [langfuse_handler]}
)
```

### 7.3 Décorateur @observe()

```python
from langfuse import observe, get_client

langfuse = get_client()

@observe()
def my_instrumented_function(input):
    output = my_llm_call(input)

    langfuse.update_current_trace(
        input=input,
        output=output,
        user_id="user_123",
        session_id="session_abc",
        tags=["agent", "my-trace"],
        metadata={"email": "user@langfuse.com"},
        version="1.0.0"
    )

    return output
```

### 7.4 Context Manager avec Spans

```python
from langfuse import get_client
from langfuse.langchain import CallbackHandler

langfuse = get_client()

with langfuse.start_as_current_span(name="multi-step-process") as root_span:
    root_span.update_trace(
        session_id="session-1234",
        user_id="user-5678",
        input={"user_query": "Explain quantum computing"}
    )

    langfuse_handler = CallbackHandler()

    # Step 1: Preprocessing
    with langfuse.start_as_current_span(name="input-preprocessing") as prep_span:
        processed_input = preprocess(user_input)
        prep_span.update(output={"processed_query": processed_input})

    # Step 2: LangChain processing
    result = chain.invoke(
        {"input": processed_input},
        config={"callbacks": [langfuse_handler]}
    )

    # Update trace output
    root_span.update_trace(output={"final_answer": result})

# Flush pour applications courtes
langfuse.flush()
```

### 7.5 Tracking Tokens et Coûts

```python
generation.update(
    output=response.content,
    usage_details={
        "input": response.usage.input_tokens,
        "output": response.usage.output_tokens,
        "cache_read_input_tokens": response.usage.cache_read_input_tokens
    },
    cost_details={
        "input": 1,
        "cache_read_input_tokens": 0.5,
        "output": 1,
    }
)
```

### 7.6 Métriques Capturées Automatiquement

- Tokens (input, output, total)
- Coût (calculé automatiquement)
- Latence par span
- Inputs/Outputs complets

---

## 8. Embedding Models

### 8.1 Comparaison des Modèles

| Modèle | Score MTEB | Dimensions | Mémoire | Vitesse |
|--------|------------|------------|---------|---------|
| mxbai-embed-large | **64.68** | 1,024 | 1.2 GB | Rapide |
| bge-m3 | 63.0 | Variable | 2-3 GB | Moyenne |
| nomic-embed-text | 53.01 | 1,024 | **0.5 GB** | Très rapide |
| all-minilm | 56.3 | 384 | 0.3 GB | **Ultra rapide** |

### 8.2 Recommandations par Cas d'Usage

| Cas d'Usage | Modèle Recommandé |
|-------------|-------------------|
| Production RAG | mxbai-embed-large |
| Multilingue (FR/EN) | **bge-m3** |
| Ressources limitées | nomic-embed-text |
| Prototypage rapide | all-minilm |

### 8.3 Configuration avec Ollama

```python
from langchain_ollama import OllamaEmbeddings

# nomic-embed-text (recommandé pour équilibre)
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434"
)

# mxbai-embed-large (meilleure qualité)
embeddings_quality = OllamaEmbeddings(
    model="mxbai-embed-large",
    base_url="http://localhost:11434"
)
```

### 8.4 Performance par Hardware

| Hardware | nomic-embed-text | mxbai-embed-large |
|----------|------------------|-------------------|
| RTX 4090 (24GB) | 12,450 tokens/sec | 8,920 tokens/sec |
| Apple M2 Max | 9,340 tokens/sec | 6,780 tokens/sec |
| Intel i9-13900K | 3,250 tokens/sec | 2,100 tokens/sec |

---

## 9. Conversation Memory

### 9.1 Short-term Memory avec InMemorySaver

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph

checkpointer = InMemorySaver()

builder = StateGraph(...)
graph = builder.compile(checkpointer=checkpointer)

graph.invoke(
    {"messages": [{"role": "user", "content": "hi! i am Bob"}]},
    {"configurable": {"thread_id": "1"}}
)
```

### 9.2 PostgreSQL Persistence

```python
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph, MessagesState, START

DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    def call_model(state: MessagesState):
        response = model.invoke(state["messages"])
        return {"messages": response}

    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_edge(START, "call_model")

    graph = builder.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "1"}}

    for chunk in graph.stream(
        {"messages": [{"role": "user", "content": "hi! I'm bob"}]},
        config,
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()
```

### 9.3 Long-term Memory avec Store

```python
from langgraph.store.postgres import PostgresStore
from langgraph.store.base import BaseStore

with (
    PostgresStore.from_conn_string(DB_URI) as store,
    PostgresSaver.from_conn_string(DB_URI) as checkpointer,
):
    def call_model(
        state: MessagesState,
        config: RunnableConfig,
        *,
        store: BaseStore,
    ):
        user_id = config["configurable"]["user_id"]
        namespace = ("memories", user_id)

        # Recherche les mémoires pertinentes
        memories = store.search(namespace, query=str(state["messages"][-1].content))
        info = "\n".join([d.value["data"] for d in memories])

        # Stocke de nouvelles mémoires si demandé
        if "remember" in state["messages"][-1].content.lower():
            store.put(namespace, str(uuid.uuid4()), {"data": "User name is Bob"})

        return {"messages": response}

    graph = builder.compile(
        checkpointer=checkpointer,
        store=store,
    )
```

### 9.4 Résumé de Conversation

```python
def summarize_conversation(state: State):
    summary = state.get("summary", "")

    if summary:
        summary_message = (
            f"This is a summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        summary_message = "Create a summary of the conversation above:"

    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)

    # Supprime tous les messages sauf les 2 plus récents
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}
```

### 9.5 Options de Persistance

| Checkpointer | Usage | Package |
|--------------|-------|---------|
| `InMemorySaver` | Développement/Tests | `langgraph.checkpoint.memory` |
| `PostgresSaver` | Production (sync) | `langgraph-checkpoint-postgres` |
| `AsyncRedisSaver` | Production (async) | `langgraph.checkpoint.redis.aio` |

---

## 10. Docker Deployment

### 10.1 Docker Compose Complet

```yaml
version: "3.9"

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
      - OLLAMA_NUM_PARALLEL=4
      - OLLAMA_MAX_LOADED_MODELS=3
      - OLLAMA_KEEP_ALIVE=10m
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    networks:
      - ai-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "wget -q --spider http://localhost:11434/api/tags || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s

  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - ai-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:6333/readyz || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: fastapi-app
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - QDRANT_HOST=http://qdrant:6333
    depends_on:
      ollama:
        condition: service_healthy
      qdrant:
        condition: service_healthy
    networks:
      - ai-network
    restart: unless-stopped

networks:
  ai-network:
    driver: bridge

volumes:
  ollama_data:
  qdrant_data:
```

### 10.2 Installation NVIDIA Container Toolkit

```bash
# Prérequis
sudo apt-get update && sudo apt-get install -y curl gnupg2

# Ajouter le repository
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Installer
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configurer Docker
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Vérifier
sudo docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

### 10.3 Variables d'Environnement Ollama

| Variable | Description | Défaut |
|----------|-------------|--------|
| `OLLAMA_NUM_PARALLEL` | Requêtes parallèles par modèle | 4 ou 1 (auto) |
| `OLLAMA_MAX_LOADED_MODELS` | Modèles chargés simultanément | 3 × GPUs |
| `OLLAMA_MAX_QUEUE` | File d'attente max | 512 |
| `OLLAMA_KEEP_ALIVE` | Durée en mémoire | 5m |
| `OLLAMA_GPU_OVERHEAD` | Mémoire GPU réservée système | - |
| `OLLAMA_DEBUG` | Niveau de debug (1-2) | 0 |

### 10.4 Apple Silicon (M1/M2/M3/M4)

**Limitation**: Docker Desktop sur macOS NE supporte PAS le GPU passthrough.

**Solution**: Architecture hybride avec Ollama natif.

```yaml
# Services auxiliaires en Docker, Ollama natif
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"

  app:
    build: ./app
    environment:
      # Connexion à Ollama natif via host.docker.internal
      - OLLAMA_HOST=http://host.docker.internal:11434
      - QDRANT_HOST=http://qdrant:6333
```

---

## 11. Semantic Chunking

### 11.1 MarkdownHeaderTextSplitter

```python
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

headers_to_split_on = [
    ("#", "title"),
    ("##", "section"),
    ("###", "subsection"),
]

md_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False
)

header_splits = md_splitter.split_text(markdown_content)

# Re-split les gros chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

final_chunks = text_splitter.split_documents(header_splits)
```

### 11.2 Préservation des Blocs de Code

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

# Splitter spécifique au code Python
python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=2000,
    chunk_overlap=200
)
```

### 11.3 Gestion des Tables

- Extraire les tables comme unités complètes (pas ligne par ligne)
- Outils recommandés: pandas, pdfplumber, Camelot
- Reformater les tables pour faciliter le traitement LLM

### 11.4 Pipeline Complet

```python
def chunk_technical_documentation(markdown_content: str):
    """Pipeline de chunking pour documentation technique."""

    # Étape 1: Split par structure Markdown
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "title"),
            ("##", "section"),
            ("###", "subsection"),
        ],
        strip_headers=False
    )
    header_splits = md_splitter.split_text(markdown_content)

    # Étape 2: Re-split les gros chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    final_chunks = text_splitter.split_documents(header_splits)

    # Étape 3: Enrichir metadata
    for i, chunk in enumerate(final_chunks):
        chunk.metadata["chunk_id"] = i
        chunk.metadata["char_count"] = len(chunk.page_content)

    return final_chunks
```

---

## 12. Error Handling & Resilience

### 12.1 Retry Logic avec Tenacity

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.ConnectError, httpx.TimeoutException))
)
def invoke_with_retry(llm, messages):
    return llm.invoke(messages)
```

### 12.2 LangChain with_retry

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen2.5:7b")

llm_with_retry = llm.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)

response = llm_with_retry.invoke(messages)
```

### 12.3 Fallback avec Modèles Alternatifs

```python
# Modèle principal
primary_llm = ChatOllama(model="qwen2.5:14b")

# Modèle de secours (plus léger)
fallback_llm = ChatOllama(model="qwen2.5:7b")

# Configuration avec fallback
llm_with_fallback = primary_llm.with_fallbacks([fallback_llm])

# Utilise automatiquement le fallback si le modèle principal échoue
response = llm_with_fallback.invoke(messages)
```

### 12.4 Health Check Ollama

```python
import httpx

def check_ollama_health(base_url: str = "http://localhost:11434") -> bool:
    try:
        response = httpx.get(f"{base_url}/api/tags", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def get_available_models(base_url: str = "http://localhost:11434") -> list:
    try:
        response = httpx.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            return [m["name"] for m in response.json().get("models", [])]
    except Exception:
        pass
    return []
```

### 12.5 Input Validation

```python
from pydantic import BaseModel, field_validator

class ChatInput(BaseModel):
    message: str
    max_tokens: int = 1000

    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Message cannot be empty')
        if len(v) > 5000:
            raise ValueError('Message too long (max 5000 chars)')
        # Sanitization basique
        v = v.replace('\x00', '')
        return v
```

---

## 13. Web Scraping Documentation

### 13.1 BeautifulSoup Pattern

```python
from bs4 import BeautifulSoup
import requests

response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")

# Supprimer le bruit
for el in soup(["script", "style", "nav", "footer"]):
    el.decompose()

# Extraire contenu principal
main = soup.select_one("article, .docs-content, main")
```

### 13.2 Extraction Hiérarchique

```python
def build_hierarchy(soup):
    structure = []
    current = None
    for el in soup.select("h1, h2, h3, p"):
        if el.name.startswith("h"):
            current = {"level": int(el.name[1]), "title": el.get_text(strip=True), "content": []}
            structure.append(current)
        elif current:
            current["content"].append(el.get_text(strip=True))
    return structure
```

### 13.3 Rate Limiting Éthique

```python
import time, random

def fetch_polite(url):
    time.sleep(random.uniform(1, 3))
    return requests.get(url, headers={"User-Agent": "DocScraper/1.0"})
```

### 13.4 Sitemap Parsing

```python
sitemap = BeautifulSoup(requests.get(sitemap_url).content, "xml")
urls = [loc.text for loc in sitemap.find_all("loc")]
```

### 13.5 Pipeline Complet de Scraping

```python
import requests
from bs4 import BeautifulSoup
import time
import random

class DocumentationScraper:
    def __init__(self, base_url: str, delay: tuple = (1, 3)):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "DocScraper/1.0"})

    def fetch(self, url: str) -> BeautifulSoup:
        time.sleep(random.uniform(*self.delay))
        response = self.session.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, "lxml")

    def clean(self, soup: BeautifulSoup) -> BeautifulSoup:
        for el in soup(["script", "style", "nav", "footer", "aside"]):
            el.decompose()
        return soup

    def extract_content(self, soup: BeautifulSoup) -> dict:
        main = soup.select_one("article, .docs-content, main, .content")
        if not main:
            main = soup.body

        return {
            "title": soup.title.string if soup.title else "",
            "content": main.get_text(separator="\n", strip=True),
            "hierarchy": self.build_hierarchy(main)
        }

    def build_hierarchy(self, element) -> list:
        structure = []
        current = None
        for el in element.select("h1, h2, h3, h4, p, li"):
            if el.name.startswith("h"):
                current = {
                    "level": int(el.name[1]),
                    "title": el.get_text(strip=True),
                    "content": []
                }
                structure.append(current)
            elif current:
                text = el.get_text(strip=True)
                if text:
                    current["content"].append(text)
        return structure

    def get_sitemap_urls(self, sitemap_url: str) -> list:
        soup = BeautifulSoup(self.session.get(sitemap_url).content, "xml")
        return [loc.text for loc in soup.find_all("loc")]
```

---

## Annexe A: Prompt Templates RAG

### System Prompt Principal

```python
SYSTEM_PROMPT = """
You are an AI assistant for Infomaniak products.
Answer questions using ONLY the provided documentation context.
If the answer is not in the context, say so clearly.
Always cite your sources.

Context:
{context}

Rules:
- Be concise and helpful
- Use bullet points for steps
- Respond in the same language as the question
- If unsure, acknowledge limitations
"""
```

### Prompt Template Complet

```python
SYSTEM_PROMPT = """You are a helpful assistant for Infomaniak documentation.

### Language
Respond in the same language as the query (French or English).

### Grounding Rules
1. Use ONLY information from the provided context
2. NEVER invent information not present
3. Cite sources using [doc_id] format

### When Information is Missing
Say: "Je n'ai pas trouvé cette information dans la documentation."
Do NOT make up information.

Context: {context}
"""
```

### Few-Shot Example

```
Query: Comment partager un dossier?
Context: [1] "Pour partager, cliquez sur..."
Answer: Pour partager un dossier, cliquez sur le bouton Partager.[1]
```

### Techniques Clés

- Chain-of-Thought pour raisonnement
- Citations inline [id]
- Détection automatique de la langue
- Fallback explicite si info manquante

---

## Annexe B: Commandes Utiles

```bash
# Ollama
ollama list                    # Liste les modèles
ollama ps                      # Modèles en mémoire
ollama pull qwen2.5:7b        # Télécharger un modèle
ollama stop <model>           # Décharger un modèle

# Docker
docker compose up -d          # Démarrer les services
docker compose logs -f        # Suivre les logs
docker compose ps             # État des services

# Qdrant
curl http://localhost:6333/collections  # Liste des collections
curl http://localhost:6333/healthz      # Health check
```

---

## Annexe C: Dépendances

```txt
# requirements.txt
langchain>=0.3.0
langchain-ollama>=0.2.0
langchain-qdrant>=0.2.0
langchain-community>=0.3.0
langgraph>=0.2.0
langgraph-checkpoint-postgres>=0.1.0
qdrant-client>=1.12.0
fastapi>=0.115.0
uvicorn>=0.32.0
pydantic>=2.10.0
langfuse>=2.50.0
beautifulsoup4>=4.12.0
lxml>=5.3.0
requests>=2.32.0
python-dotenv>=1.0.0
tenacity>=8.2.0
httpx>=0.27.0
sentence-transformers>=2.5.0
ragas>=0.1.0
```

---

## Annexe D: Architecture Finale

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   FastAPI   │────▶│  LangChain  │
│  (Web/CLI)  │     │   :8000     │     │    Agent    │
└─────────────┘     └─────────────┘     └──────┬──────┘
                           │                   │
                    ┌──────┴──────┐     ┌──────┴──────┐
                    │  Langfuse   │     │    Tools    │
                    │  (Tracing)  │     │  (RAG, etc) │
                    └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
             ┌──────┴──────┐           ┌───────┴───────┐          ┌───────┴───────┐
             │   Qdrant    │           │    Ollama     │          │    Ollama     │
             │   :6333     │           │  Embeddings   │          │   Chat LLM    │
             │  (Vectors)  │           │ nomic-embed   │          │  qwen2.5:7b   │
             └─────────────┘           └───────────────┘          └───────────────┘
```

---

*Document fusionné généré le 15/01/2026 - Infomaniak Documentation AI Assistant*
