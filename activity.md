# Activity Log - Infomaniak Doc Assistant

## Project Information
- **Started**: 2026-01-16
- **Goal**: Build production-ready AI assistant for Infomaniak documentation
- **Stack**: FastAPI, LangChain, Qdrant, Ollama/Mistral/Qwen

---

## Progress Log

<!--
Template for each task entry:

### [TIMESTAMP] - Task: [TASK_ID]
**Status**: in_progress | completed | failed
**Description**: [Brief description of what was done]

**Actions Taken**:
- Action 1
- Action 2

**Verification**:
- Command/test run: `[command]`
- Result: [pass/fail with details]

**Files Modified**:
- path/to/file1.py
- path/to/file2.py

**Notes**:
- Any observations, issues, or decisions

**Screenshot**: screenshots/[task-id].png (if applicable)

---
-->

<!-- Progress entries will be added below this line -->

### 2026-01-16 - Task: llm-001
**Status**: completed
**Description**: Created app/llm/base.py with abstract LLMProvider class

**Actions Taken**:
- Read docs/reference/04-ollama.md for LLM patterns
- Created abstract base class LLMProvider with ABC
- Defined abstract methods: get_chat_model() returning BaseChatModel, get_embeddings() returning Embeddings
- Used type hints from langchain_core

**Verification**:
- Command: `uv run python -c "from app.llm.base import LLMProvider; print(LLMProvider)"`
- Result: PASS - Output: `<class 'app.llm.base.LLMProvider'>`

**Files Modified**:
- app/llm/base.py (created)

**Notes**:
- Used langchain_core.embeddings.Embeddings and langchain_core.language_models.chat_models.BaseChatModel for type hints
- Abstract methods use `...` as placeholder (Pythonic convention)

---

### 2026-01-16 - Task: llm-002
**Status**: completed
**Description**: Created app/llm/ollama_provider.py with OllamaProvider class

**Actions Taken**:
- Read docs/reference/04-ollama.md for Ollama patterns
- Created OllamaProvider class extending LLMProvider
- Implemented get_chat_model() returning ChatOllama with settings
- Implemented get_embeddings() returning OllamaEmbeddings with settings

**Verification**:
- Command: `uv run python -c "from app.llm.ollama_provider import OllamaProvider; print(OllamaProvider)"`
- Result: PASS - Output: `<class 'app.llm.ollama_provider.OllamaProvider'>`

**Files Modified**:
- app/llm/ollama_provider.py (created)

**Notes**:
- Used ChatOllama with temperature=0.7, num_ctx=4096
- Configuration values come from app.config.settings

---

### 2026-01-16 - Task: config-001
**Status**: completed
**Description**: Created app/config.py with Pydantic Settings

**Actions Taken**:
- Read docs/reference/11-pydantic-settings.md for reference patterns
- Read .env.example to get all environment variables
- Created app/config.py with Settings class using pydantic_settings.BaseSettings
- Included all env vars: LLM provider, Ollama, Qwen API, Mistral API, Qdrant, App, Langfuse, RAG, Jina

**Verification**:
- Command: `uv run python -c "from app.config import settings; print(settings.LLM_PROVIDER)"`
- Result: PASS - Output: `ollama`

**Files Modified**:
- app/config.py (created)

**Notes**:
- Used model_config dict with env_file, env_file_encoding, and extra="ignore"
- All settings have sensible defaults matching .env.example

---

### 2026-01-16 - Task: llm-003
**Status**: completed
**Description**: Created app/llm/mistral_provider.py with MistralAPIProvider class

**Actions Taken**:
- Read docs/reference/04-ollama.md for LLM patterns
- Created MistralAPIProvider class extending LLMProvider
- Implemented get_chat_model() returning ChatMistralAI with settings
- Implemented get_embeddings() returning MistralAIEmbeddings with settings

**Verification**:
- Command: `uv run python -c "from app.llm.mistral_provider import MistralAPIProvider; print(MistralAPIProvider)"`
- Result: PASS - Output: `<class 'app.llm.mistral_provider.MistralAPIProvider'>`

**Files Modified**:
- app/llm/mistral_provider.py (created)

**Notes**:
- Used ChatMistralAI and MistralAIEmbeddings from langchain_mistralai
- Configuration values come from app.config.settings (MISTRAL_API_KEY, MISTRAL_CHAT_MODEL, MISTRAL_EMBEDDING_MODEL)

---

### 2026-01-16 - Task: llm-004
**Status**: completed
**Description**: Created app/llm/factory.py and wired up __init__.py exports

**Actions Taken**:
- Created app/llm/factory.py with get_provider() function
- Implemented provider selection based on LLM_PROVIDER config (supports "ollama" and "mistral")
- Added get_chat_model() and get_embeddings() helper functions
- Updated app/llm/__init__.py to export get_provider, get_chat_model, get_embeddings

**Verification**:
- Command: `uv run python -c "from app.llm import get_chat_model; print(get_chat_model)"`
- Result: PASS - Output: `<function get_chat_model at 0x105f8c540>`

**Files Modified**:
- app/llm/factory.py (created)
- app/llm/__init__.py (updated)

**Notes**:
- Factory pattern allows easy extension for new providers
- ValueError raised for unsupported providers

---

### 2026-01-16 - Task: api-001
**Status**: completed
**Description**: Created app/main.py with FastAPI app and /health endpoint

**Actions Taken**:
- Read docs/reference/06-fastapi.md for FastAPI patterns
- Created FastAPI app instance with title, description, version
- Added CORS middleware with allow_origins=["*"]
- Added /health GET endpoint returning {"status": "ok"}

**Verification**:
- Command: `uv run uvicorn app.main:app --port 8000 & sleep 3 && curl -s localhost:8000/health && pkill -f uvicorn`
- Result: PASS - Output: `{"status":"ok"}`

**Files Modified**:
- app/main.py (created)

**Notes**:
- Used allow_origins=["*"] for development flexibility
- Endpoint returns dict[str, str] with type hint

---

### 2026-01-16 - Task: models-001
**Status**: completed
**Description**: Created app/models/schemas.py with Pydantic models

**Actions Taken**:
- Read docs/reference/05-pydantic.md for Pydantic patterns
- Created ChatRequest model with message (str, min_length=1, max_length=5000) and session_id (str | None)
- Created ChatResponse model with answer (str) and sources (list[str])
- Created HealthResponse model with status (str)

**Verification**:
- Command: `uv run python -c "from app.models.schemas import ChatRequest; print(ChatRequest(message='test'))"`
- Result: PASS - Output: `message='test' session_id=None`

**Files Modified**:
- app/models/schemas.py (created)

**Notes**:
- Used Field(...) with min_length and max_length for message validation
- Used Field(default_factory=list) for sources to avoid mutable default

---

### 2026-01-16 - Task: rag-001
**Status**: completed
**Description**: Created app/rag/embeddings.py with embedding functions

**Actions Taken**:
- Read docs/reference/02-rag-pipeline.md and docs/reference/08-embeddings.md for patterns
- Created app/rag/embeddings.py with embed_text() and embed_documents() functions
- Used get_embeddings() from app.llm to get the embeddings provider
- Used embed_query() for single text and embed_documents() for multiple texts

**Verification**:
- Command: `uv run python -c "from app.rag.embeddings import embed_text; print(type(embed_text))"`
- Result: PASS - Output: `<class 'function'>`

**Files Modified**:
- app/rag/embeddings.py (created)

**Notes**:
- Functions delegate to the configured LLM provider's embedding model
- Returns list[float] for single text, list[list[float]] for multiple texts

---

### 2026-01-16 - Task: rag-002
**Status**: completed
**Description**: Created app/rag/chunker.py with text chunking function

**Actions Taken**:
- Read docs/reference/02-rag-pipeline.md for chunking patterns
- Created app/rag/chunker.py with chunk_text() function
- Used RecursiveCharacterTextSplitter with chunk_size=500, chunk_overlap=50
- Returns list of Document objects with metadata attached to each chunk

**Verification**:
- Command: `uv run python -c "from app.rag.chunker import chunk_text; print(len(chunk_text('test ' * 200, {})))"`
- Result: PASS - Output: `3`

**Files Modified**:
- app/rag/chunker.py (created)

**Notes**:
- Uses separators ["##", "###", "\n\n", "\n", ". ", " "] for markdown-aware splitting
- Returns langchain_core.documents.Document objects for compatibility with LangChain

---

### 2026-01-16 - Task: rag-003
**Status**: completed
**Description**: Created app/rag/retriever.py with QdrantRetriever class

**Actions Taken**:
- Read docs/reference/03-qdrant.md for Qdrant patterns
- Created QdrantRetriever class with __init__ connecting to Qdrant using settings
- Implemented create_collection() method (768 dimensions for nomic-embed-text, COSINE distance)
- Implemented upsert(chunks) method that embeds documents and stores them in Qdrant

**Verification**:
- Command: `uv run python -c "from app.rag.retriever import QdrantRetriever; print(QdrantRetriever)"`
- Result: PASS - Output: `<class 'app.rag.retriever.QdrantRetriever'>`

**Files Modified**:
- app/rag/retriever.py (created)

**Notes**:
- Uses uuid.uuid4() for unique point IDs
- Stores payload with content, source, title, and product metadata
- Checks if collection exists before creating to avoid errors

---

### 2026-01-16 - Task: rag-004
**Status**: completed
**Description**: Added search method to QdrantRetriever class

**Actions Taken**:
- Read docs/reference/03-qdrant.md for Qdrant search patterns
- Implemented search(query: str, top_k: int = 5) method in QdrantRetriever
- Method embeds the query using embed_text() and searches Qdrant
- Returns list of Document objects with content and metadata including score
- Handles empty results gracefully by returning empty list

**Verification**:
- Command: `uv run python -c "from app.rag.retriever import QdrantRetriever; r = QdrantRetriever(); print(hasattr(r, 'search'))"`
- Result: PASS - Output: `True`

**Files Modified**:
- app/rag/retriever.py (updated)

**Notes**:
- Uses client.search() with with_payload=True to get document content
- Score is included in document metadata for ranking
- Returns langchain_core.documents.Document for LangChain compatibility

---

### 2026-01-16 - Task: ingest-001
**Status**: completed
**Description**: Created scripts/ingest.py to load docs from data/docs/

**Actions Taken**:
- Read docs/reference/03-qdrant.md for reference patterns
- Created load_documents(directory: str) function to read .md files recursively
- Parses each file: extracts title (line 1 after #), source URL (line 3 after Source:), content (after ---)
- Returns list of dicts with keys: title, source, product, content
- Added argparse with --source (default: data/docs) and --dry-run flags

**Verification**:
- Command: `uv run python scripts/ingest.py --dry-run | head -20`
- Result: PASS - Found 60 documents with correct parsing of title, source, product, and content

**Files Modified**:
- scripts/ingest.py (created)

**Notes**:
- Uses pathlib.Path.rglob("*.md") for recursive file discovery
- Product is extracted from parent folder name (kchat, kmeet, kdrive)
- Dry run mode shows first 5 documents with preview

---

### 2026-01-16 - Task: ingest-002
**Status**: completed
**Description**: Added chunking and Qdrant ingestion to ingest.py

**Actions Taken**:
- Imported chunker and QdrantRetriever from app.rag
- Added ingestion logic in else branch (when not dry-run)
- Creates collection if it doesn't exist (768 dimensions for nomic-embed-text)
- Chunks all documents using chunk_text() preserving metadata (source, product, title)
- Embeds chunks and upserts to Qdrant using retriever.upsert()
- Shows progress with count of documents, chunks, and ingested points

**Verification**:
- Command: `uv run python scripts/ingest.py --source data/docs && curl -s localhost:6333/collections/infomaniak_docs | grep points_count`
- Result: PASS - Output shows 579 chunks created from 60 documents, and Qdrant collection contains `"points_count":579`

**Files Modified**:
- scripts/ingest.py (updated)

**Notes**:
- Ingestion takes a few seconds due to embedding generation
- Each chunk preserves original document metadata for source citation
- Collection uses COSINE distance metric

---

### 2026-01-16 - Task: agent-001
**Status**: completed
**Description**: Created app/agent/prompts.py with SYSTEM_PROMPT constant

**Actions Taken**:
- Read docs/reference/01-langchain-agents.md for agent patterns
- Read docs/prd.md Appendix B for sample prompt template
- Created app/agent/prompts.py with SYSTEM_PROMPT constant
- Included rules: use only context, cite sources, respond in query language, acknowledge limitations

**Verification**:
- Command: `uv run python -c "from app.agent.prompts import SYSTEM_PROMPT; print(SYSTEM_PROMPT[:50])"`
- Result: PASS - Output: `You are an AI assistant for Infomaniak products (k`

**Files Modified**:
- app/agent/prompts.py (created)

**Notes**:
- Prompt mentions all three products: kDrive, kMeet, kChat
- Includes instruction to cite sources with URLs
- Suggests contacting Infomaniak support when unsure

---

### 2026-01-16 - Task: agent-002
**Status**: completed
**Description**: Created app/agent/tools.py with search_docs tool

**Actions Taken**:
- Read docs/reference/01-langchain-agents.md for tool patterns
- Created app/agent/tools.py with search_docs tool using @tool(parse_docstring=True)
- Tool uses QdrantRetriever to search documentation
- Formats results with title, product, content, and source citation

**Verification**:
- Command: `uv run python -c "from app.agent.tools import search_docs; print(search_docs.name)"`
- Result: PASS - Output: `search_docs`

**Files Modified**:
- app/agent/tools.py (created)

**Notes**:
- Tool returns formatted results with markdown formatting
- Includes source URLs for citation
- Returns "No relevant documentation found" message when no results

---

### 2026-01-16 - Task: agent-003
**Status**: completed
**Description**: Created app/agent/executor.py with get_agent() function

**Actions Taken**:
- Read docs/reference/01-langchain-agents.md for ReAct agent patterns
- Created app/agent/executor.py with get_agent() function
- Used create_react_agent from langgraph.prebuilt
- Added InMemorySaver as checkpointer for conversation memory
- Wired together model, tools, and system prompt

**Verification**:
- Command: `uv run python -c "from app.agent.executor import get_agent; print(get_agent)"`
- Result: PASS - Output: `<function get_agent at 0x105181580>`

**Files Modified**:
- app/agent/executor.py (created)

**Notes**:
- Uses module-level _checkpointer for memory persistence across calls
- Agent uses search_docs tool and SYSTEM_PROMPT from other agent modules
- Model comes from app.llm.get_chat_model() for provider-agnostic usage

---

### 2026-01-16 - Task: api-002
**Status**: completed
**Description**: Added POST /chat endpoint to app/main.py

**Actions Taken**:
- Read docs/reference/06-fastapi.md for FastAPI endpoint patterns
- Read docs/reference/01-langchain-agents.md for agent invocation patterns
- Added imports for ChatRequest, ChatResponse, get_agent, uuid
- Implemented /chat POST endpoint with async ainvoke on agent
- Used session_id for thread-based conversation memory (generates UUID if not provided)
- Extracts answer from last AI message and sources from tool responses

**Verification**:
- Command: `curl -X POST localhost:8000/chat -H 'Content-Type: application/json' -d '{"message":"test"}'`
- Result: PASS - Output: `{"answer":"It seems like you might be testing the system or looking for assistance. How can I help you today? 😊","sources":[]}`

**Files Modified**:
- app/main.py (updated)

**Notes**:
- Agent invoked with ainvoke for async support
- Sources extracted by parsing tool message content for "Source:" lines
- Response model enforced with response_model=ChatResponse

---

### 2026-01-16 - Task: api-003
**Status**: completed
**Description**: Added GET /chat/stream endpoint with SSE streaming

**Actions Taken**:
- Read docs/reference/06-fastapi.md for SSE patterns
- Added json import and StreamingResponse import
- Created format_sse() helper function to format data as SSE events
- Created sse_stream() async generator using agent.astream_events() with version="v2"
- Implemented /chat/stream GET endpoint returning StreamingResponse with text/event-stream media type

**Verification**:
- Command: `curl -N 'localhost:8000/chat/stream?message=hello' | head -20`
- Result: PASS - Output shows streaming tokens: `data: {"token": "Hello"}`, `data: {"token": "!"}`, etc.

**Files Modified**:
- app/main.py (updated)

**Notes**:
- Uses astream_events with version="v2" for LangGraph streaming
- Filters for "on_chat_model_stream" events to extract AI tokens
- Final event sends {"done": True} to signal stream completion

---

### 2026-01-16 - Task: obs-001
**Status**: completed
**Description**: Created app/observability/langfuse.py with get_langfuse_handler() function

**Actions Taken**:
- Read docs/reference/07-langfuse.md for Langfuse patterns
- Created app/observability/langfuse.py with get_langfuse_handler() function
- Function returns CallbackHandler when LANGFUSE_ENABLED is true, None otherwise
- Used langfuse.langchain.CallbackHandler import (updated from reference which had older import path)

**Verification**:
- Command: `uv run python -c "from app.observability.langfuse import get_langfuse_handler; print(get_langfuse_handler())"`
- Result: PASS - Output: `None` (correct because LANGFUSE_ENABLED defaults to False)

**Files Modified**:
- app/observability/langfuse.py (created)

**Notes**:
- Import path is `langfuse.langchain.CallbackHandler` (not `langfuse.callback` as in older docs)
- Handler is configured with public_key, secret_key, and host from settings
- Returns None when disabled to avoid unnecessary API calls

---

### 2026-01-16 - Task: obs-002
**Status**: completed
**Description**: Added GET /metrics endpoint with request and error counters

**Actions Taken**:
- Read docs/reference/06-fastapi.md and docs/reference/07-langfuse.md for patterns
- Added simple in-memory metrics dict with request_count and error_count
- Added /metrics GET endpoint returning the metrics dict as JSON
- Updated /chat endpoint to increment request_count on each call
- Added try/except to increment error_count on exceptions

**Verification**:
- Command: `curl localhost:8000/metrics`
- Result: PASS - Output: `{"request_count":0,"error_count":0}`

**Files Modified**:
- app/main.py (updated)

**Notes**:
- Simple in-memory metrics reset on server restart
- Counters track all /chat requests and errors

---

### 2026-01-16 - Task: obs-003
**Status**: completed
**Description**: Added error handling middleware with exception handlers

**Actions Taken**:
- Read docs/reference/06-fastapi.md for exception handler patterns
- Added RequestValidationError exception handler returning 400 with error details
- Added general Exception handler returning 500 with "Internal server error"
- Added logging for both error types using Python's logging module

**Verification**:
- Command: `curl -X POST localhost:8000/chat -d 'invalid'`
- Result: PASS - Returns HTTP 400 with `{"detail":[{"type":"json_invalid",...}]}`
- Command: `curl -X POST localhost:8000/chat -H 'Content-Type: application/json' -d '{}'`
- Result: PASS - Returns HTTP 400 with `{"detail":[{"type":"missing","loc":["body","message"],...}]}`

**Files Modified**:
- app/main.py (updated)

**Notes**:
- Used RequestValidationError from fastapi.exceptions for validation errors
- Errors are logged with logger.error() for observability
- Returns JSONResponse with appropriate status codes

---

### 2026-01-16 - Task: test-001
**Status**: completed
**Description**: Created tests/test_api.py with API endpoint tests

**Actions Taken**:
- Added pytest and httpx as dev dependencies
- Created tests/test_api.py with TestClient from fastapi.testclient
- Implemented test_health_returns_200() to verify health endpoint
- Implemented test_chat_rejects_empty_message() to verify validation

**Verification**:
- Command: `uv run pytest tests/test_api.py -v`
- Result: PASS - 2 tests passed

**Files Modified**:
- tests/test_api.py (created)
- pyproject.toml (updated with pytest, httpx deps)

**Notes**:
- TestClient used for synchronous testing of FastAPI app
- Empty message validation triggers 400 response (min_length=1 constraint)

---

### 2026-01-16 - Task: test-002
**Status**: completed
**Description**: Created tests/test_rag.py with RAG component tests

**Actions Taken**:
- Created tests/test_rag.py with pytest
- Implemented test_chunker_splits_text() to verify text chunking and metadata preservation
- Implemented test_retriever_initializes() to verify QdrantRetriever initialization
- Added skip logic if Qdrant is unavailable

**Verification**:
- Command: `uv run pytest tests/test_rag.py -v`
- Result: PASS - 2 tests passed

**Files Modified**:
- tests/test_rag.py (created)

**Notes**:
- Chunker test verifies text is split into multiple chunks with metadata attached
- Retriever test checks initialization and presence of required methods
- Uses pytest.skip() to gracefully handle unavailable Qdrant server

---

### 2026-01-16 - Task: ui-001
**Status**: completed
**Description**: Created static/index.html with basic chat form and mounted static files in FastAPI

**Actions Taken**:
- Created static/ directory
- Created static/index.html with HTML structure: header, chat container, input form
- Added minimal CSS styling: Infomaniak blue theme (#0066cc), responsive layout, message bubbles
- Imported StaticFiles from fastapi.staticfiles
- Added app.mount("/static", StaticFiles(directory="static"), name="static")

**Verification**:
- Command: `curl localhost:8000/static/index.html`
- Result: PASS - HTTP 200, returns full HTML content

**Files Modified**:
- static/index.html (created)
- app/main.py (updated with static file mount)

**Notes**:
- Script tag placeholder added for ui-002 JavaScript implementation
- CSS uses system font stack for cross-platform consistency
- Chat container has min-height for initial display before messages

---

### 2026-01-16 - Task: ui-002
**Status**: completed
**Description**: Added JavaScript to chat UI for POST /chat interaction

**Actions Taken**:
- Added JavaScript to static/index.html with fetch() call to POST /chat
- Implemented addMessage() function to display messages in chat container
- Implemented sendMessage() function with loading state and error handling
- Added form submit event listener to capture user input
- Also fixed Qdrant retriever bug: changed client.search() to client.query_points() (API change)

**Verification**:
- Browser test: Opened localhost:8000/static/index.html, sent "What is kDrive?"
- Result: PASS - User message displayed in blue bubble, loading "Thinking..." shown, assistant response displayed with kDrive information
- Screenshot saved to screenshots/ui-002.png

**Files Modified**:
- static/index.html (updated with JavaScript)
- app/rag/retriever.py (fixed search method to use query_points)

**Notes**:
- JavaScript uses async/await for clean async handling
- Session ID generated with crypto.randomUUID() for conversation continuity
- Button disabled during request to prevent double-submit
- Error handling displays user-friendly message on failure

**Screenshot**: screenshots/ui-002.png

---

### 2026-01-16 - Task: ui-003
**Status**: completed
**Description**: Added streaming support to chat UI using EventSource for SSE

**Actions Taken**:
- Replaced sendMessage() with sendMessageStream() function in static/index.html
- Implemented EventSource connection to /chat/stream endpoint
- Created empty response div that gets updated with streaming tokens
- Added onmessage handler to parse SSE events and append tokens
- Added onerror handler for graceful error handling
- Updated form submit handler to use streaming function

**Verification**:
- Opened localhost:8000/static/index.html in browser
- Sent message "What is kDrive?"
- Result: PASS - Tokens streamed in real-time, response displayed progressively

**Files Modified**:
- static/index.html (updated JavaScript)

**Notes**:
- EventSource used for SSE (Server-Sent Events) streaming
- Tokens appended to response div as they arrive via data.token
- Stream completes when data.done is received
- Button disabled during streaming, re-enabled on completion

**Screenshot**: screenshots/ui-003.png

---

