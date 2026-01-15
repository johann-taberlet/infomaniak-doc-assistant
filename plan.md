# Ralph Loop Task Plan

This file contains all tasks for the Ralph Wiggum Loop to execute.
Each task should be completed one at a time, verified, and marked as `passes: true`.

```json
[
  {
    "id": "config-001",
    "category": "setup",
    "description": "Create app/config.py with Pydantic Settings for all environment variables",
    "steps": [
      "Import BaseSettings from pydantic_settings",
      "Create Settings class with all env vars from .env.example",
      "Add field validators where needed",
      "Export settings singleton",
      "Test loading with python -c 'from app.config import settings; print(settings)'"
    ],
    "verification": "python -c 'from app.config import settings; print(settings.LLM_PROVIDER)' prints 'ollama'",
    "passes": false
  },
  {
    "id": "config-002",
    "category": "setup",
    "description": "Create LLM provider abstraction with Ollama, Qwen API, and Mistral API support",
    "steps": [
      "Create app/llm/base.py with abstract LLMProvider class",
      "Create app/llm/ollama_provider.py implementing OllamaProvider",
      "Create app/llm/qwen_provider.py implementing QwenAPIProvider",
      "Create app/llm/mistral_provider.py implementing MistralAPIProvider",
      "Create app/llm/factory.py with get_llm_provider() function",
      "Export get_chat_model() and get_embeddings() from app/llm/__init__.py"
    ],
    "verification": "python -c 'from app.llm import get_chat_model, get_embeddings; print(get_chat_model())' works",
    "passes": false
  },
  {
    "id": "config-003",
    "category": "setup",
    "description": "Create app/main.py with FastAPI skeleton and /health endpoint",
    "steps": [
      "Import FastAPI and create app instance",
      "Add lifespan context manager for startup/shutdown",
      "Create GET /health endpoint returning status and version",
      "Add CORS middleware for localhost:3000",
      "Create root endpoint with API info"
    ],
    "verification": "Run 'uvicorn app.main:app --port 8000' and curl localhost:8000/health returns 200",
    "passes": false
  },
  {
    "id": "rag-001",
    "category": "feature",
    "description": "Create app/models/schemas.py with all Pydantic models",
    "steps": [
      "Create ChatRequest model (message, session_id, language)",
      "Create ChatResponse model (answer, sources, confidence)",
      "Create DocumentChunk model (content, metadata, source_url)",
      "Create HealthResponse model",
      "Create StreamEvent model for SSE",
      "Add field validators for input sanitization"
    ],
    "verification": "python -c 'from app.models.schemas import ChatRequest; print(ChatRequest(message=\"test\"))'",
    "passes": false
  },
  {
    "id": "rag-002",
    "category": "feature",
    "description": "Create app/rag/embeddings.py for embedding generation",
    "steps": [
      "Import get_embeddings from app.llm",
      "Create embed_text(text: str) function",
      "Create embed_documents(texts: list[str]) function",
      "Add retry logic with tenacity",
      "Handle connection errors gracefully"
    ],
    "verification": "python -c 'from app.rag.embeddings import embed_text; v=embed_text(\"test\"); print(len(v))' returns embedding dimension",
    "passes": false
  },
  {
    "id": "rag-003",
    "category": "feature",
    "description": "Create app/rag/chunker.py for document chunking",
    "steps": [
      "Import text splitters from langchain_text_splitters",
      "Create MarkdownHeaderTextSplitter for structure-aware splitting",
      "Create RecursiveCharacterTextSplitter for sub-chunking",
      "Implement chunk_document(content, metadata) function",
      "Use chunk_size=500 and chunk_overlap=50 from config"
    ],
    "verification": "python -c 'from app.rag.chunker import chunk_document; chunks=chunk_document(\"# Test\\n\\nContent\", {}); print(len(chunks))'",
    "passes": false
  },
  {
    "id": "rag-004",
    "category": "feature",
    "description": "Create app/rag/retriever.py for Qdrant integration",
    "steps": [
      "Import QdrantClient from qdrant_client",
      "Create QdrantRetriever class",
      "Implement create_collection() method",
      "Implement upsert_documents(chunks) method",
      "Implement search(query, top_k, filters) method",
      "Implement as_langchain_retriever() for LangChain integration"
    ],
    "verification": "python -c 'from app.rag.retriever import QdrantRetriever; r=QdrantRetriever(); print(r)'",
    "passes": false
  },
  {
    "id": "rag-005",
    "category": "feature",
    "description": "Create scripts/scraper.py for documentation scraping",
    "steps": [
      "Create DocumentationScraper class",
      "Implement fetch(url) method with rate limiting (1-3s delay)",
      "Implement clean(soup) method to remove nav/footer/scripts",
      "Implement extract_content(soup) method for text extraction",
      "Implement get_sitemap_urls(sitemap_url) method",
      "Add CLI interface with argparse",
      "Test with a single page from docs.infomaniak.com"
    ],
    "verification": "python scripts/scraper.py --url https://docs.infomaniak.com --test shows extracted content",
    "passes": false
  },
  {
    "id": "ingest-001",
    "category": "feature",
    "description": "Create scripts/ingest.py for documentation ingestion pipeline",
    "steps": [
      "Import scraper, chunker, embeddings, retriever modules",
      "Create ingest_url(url) function for single page ingestion",
      "Create ingest_sitemap(sitemap_url) function for bulk ingestion",
      "Add progress logging with counts",
      "Add CLI interface with argparse",
      "Add --dry-run option to preview without ingesting"
    ],
    "verification": "python scripts/ingest.py --help shows usage",
    "passes": false
  },
  {
    "id": "ingest-002",
    "category": "feature",
    "description": "Run documentation ingestion for Infomaniak docs",
    "steps": [
      "Ensure Qdrant is running (docker)",
      "Run ingestion for kDrive section",
      "Run ingestion for kMeet section",
      "Run ingestion for kChat section",
      "Verify documents exist in Qdrant",
      "Log total chunks indexed"
    ],
    "verification": "curl localhost:6333/collections/infomaniak_docs shows points_count > 0",
    "passes": false
  },
  {
    "id": "agent-001",
    "category": "feature",
    "description": "Create app/agent/prompts.py with system prompts",
    "steps": [
      "Create SYSTEM_PROMPT constant for RAG assistant",
      "Include grounding rules (use only context, no invention)",
      "Include language detection instruction (respond in query language)",
      "Include citation format [source_id]",
      "Include fallback instruction for missing info"
    ],
    "verification": "python -c 'from app.agent.prompts import SYSTEM_PROMPT; print(SYSTEM_PROMPT[:100])'",
    "passes": false
  },
  {
    "id": "agent-002",
    "category": "feature",
    "description": "Create app/agent/tools.py with RAG search tool",
    "steps": [
      "Import @tool decorator from langchain.tools",
      "Import QdrantRetriever from app.rag.retriever",
      "Create search_documentation(query: str) tool",
      "Format results with source citations",
      "Add docstring with parse_docstring=True"
    ],
    "verification": "python -c 'from app.agent.tools import search_documentation; print(search_documentation.name)'",
    "passes": false
  },
  {
    "id": "agent-003",
    "category": "feature",
    "description": "Create app/agent/executor.py with LangChain agent",
    "steps": [
      "Import ChatOllama/get_chat_model and create_react_agent",
      "Import tools from app.agent.tools",
      "Import prompts from app.agent.prompts",
      "Create get_agent() function returning configured agent",
      "Add InMemorySaver for conversation memory",
      "Configure with fallback for errors"
    ],
    "verification": "python -c 'from app.agent.executor import get_agent; a=get_agent(); print(type(a))'",
    "passes": false
  },
  {
    "id": "agent-004",
    "category": "feature",
    "description": "Add POST /chat endpoint to FastAPI",
    "steps": [
      "Import ChatRequest and ChatResponse from models",
      "Import get_agent from app.agent.executor",
      "Create POST /chat endpoint accepting ChatRequest",
      "Invoke agent with message and session_id as thread_id",
      "Extract answer and sources from agent response",
      "Return ChatResponse with answer, sources, confidence"
    ],
    "verification": "curl -X POST localhost:8000/chat -H 'Content-Type: application/json' -d '{\"message\":\"Bonjour\"}' returns response",
    "passes": false
  },
  {
    "id": "agent-005",
    "category": "feature",
    "description": "Add GET /chat/stream endpoint with SSE streaming",
    "steps": [
      "Create StreamingResponse generator function",
      "Format output as Server-Sent Events (SSE)",
      "Stream tokens from LLM as they arrive",
      "Handle client disconnection gracefully",
      "Send completion event at end"
    ],
    "verification": "curl -N 'localhost:8000/chat/stream?message=Bonjour' shows streaming tokens",
    "passes": false
  },
  {
    "id": "obs-001",
    "category": "feature",
    "description": "Create app/observability/langfuse.py for tracing",
    "steps": [
      "Import CallbackHandler from langfuse",
      "Create get_langfuse_handler() function",
      "Configure with environment variables",
      "Add enabled/disabled flag from config",
      "Handle missing credentials gracefully (return None)"
    ],
    "verification": "python -c 'from app.observability.langfuse import get_langfuse_handler; print(get_langfuse_handler())'",
    "passes": false
  },
  {
    "id": "obs-002",
    "category": "feature",
    "description": "Add GET /metrics endpoint",
    "steps": [
      "Create simple in-memory metrics store",
      "Track request count, error count",
      "Track latency (p50, p95, p99)",
      "Create GET /metrics endpoint returning JSON",
      "Update metrics on each /chat request"
    ],
    "verification": "curl localhost:8000/metrics returns JSON with request_count field",
    "passes": false
  },
  {
    "id": "obs-003",
    "category": "feature",
    "description": "Add error handling middleware",
    "steps": [
      "Create exception handler for RequestValidationError",
      "Create exception handler for general exceptions",
      "Log errors with stack traces",
      "Return user-friendly error messages (no internal details)",
      "Increment error metrics"
    ],
    "verification": "curl localhost:8000/chat with invalid JSON returns 400 with structured error",
    "passes": false
  },
  {
    "id": "test-001",
    "category": "testing",
    "description": "Create tests/test_api.py for API endpoint tests",
    "steps": [
      "Import TestClient from fastapi.testclient",
      "Create test_health_returns_200()",
      "Create test_chat_valid_request() (may need mock)",
      "Create test_chat_empty_message_returns_400()",
      "Create test_metrics_returns_json()"
    ],
    "verification": "pytest tests/test_api.py -v passes all tests",
    "passes": false
  },
  {
    "id": "test-002",
    "category": "testing",
    "description": "Create tests/test_rag.py for RAG pipeline tests",
    "steps": [
      "Create test_chunker_splits_markdown()",
      "Create test_retriever_search_returns_results() (needs Qdrant)",
      "Create test_embeddings_returns_vector() (needs Ollama or mock)",
      "Skip tests that require external services if not available"
    ],
    "verification": "pytest tests/test_rag.py -v passes all tests (or skips appropriately)",
    "passes": false
  },
  {
    "id": "ui-001",
    "category": "feature",
    "description": "Create static/index.html with chat UI",
    "steps": [
      "Create HTML structure with chat container",
      "Add CSS styling (clean, modern design)",
      "Add JavaScript for sending messages to /chat",
      "Display responses with source citations",
      "Add loading indicator during requests",
      "Mount static files in FastAPI app"
    ],
    "verification": "Open localhost:8000 in browser shows chat interface",
    "passes": false
  },
  {
    "id": "ui-002",
    "category": "feature",
    "description": "Add streaming support to chat UI",
    "steps": [
      "Update JavaScript to use EventSource for /chat/stream",
      "Display tokens as they arrive",
      "Handle stream completion event",
      "Add option to toggle streaming on/off"
    ],
    "verification": "Type message in UI and see response stream in real-time",
    "passes": false
  }
]
```
