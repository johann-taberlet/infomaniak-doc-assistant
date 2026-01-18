# Infomaniak Documentation AI Assistant

AI assistant for Infomaniak documentation (kDrive, kMeet, kChat, kSuite, SwissTransfer).

## Architecture

- **Backend**: FastAPI + LangChain with RAG (Retrieval Augmented Generation)
- **Frontend**: React + TypeScript + Vite
- **Vector Store**: Qdrant
- **LLM**: Ollama (local) or OpenRouter (cloud)

## Prerequisites

- Python 3.11+
- Node.js 20+
- Ollama with `qwen3:8b` and `nomic-embed-text` models
- Qdrant (via Docker)

## Installation

### 1. Clone and setup backend

```bash
# Install dependencies
uv sync

# Copy environment file
cp .env.example .env
```

### 2. Start services

```bash
# Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# Pull Ollama models
ollama pull qwen3:8b
ollama pull nomic-embed-text
```

### 3. Setup frontend

```bash
cd frontend
npm install
```

## Configuration

Edit `.env` to configure the application:

```env
# LLM Provider: "ollama" or "openrouter"
LLM_PROVIDER=ollama
LLM_TEMPERATURE=0.7

# Ollama (local)
OLLAMA_HOST=http://localhost:11434
OLLAMA_CHAT_MODEL=qwen3:8b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

# OpenRouter (cloud) - requires API key
OPENROUTER_API_KEY=
OPENROUTER_CHAT_MODEL=mistralai/ministral-8b

# Qdrant
QDRANT_HOST=http://localhost:6333
QDRANT_COLLECTION=infomaniak_docs

# Observability (optional)
LANGFUSE_ENABLED=false
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
```

## Running

### Development

```bash
# Terminal 1: Backend
uv run uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev
```

### Production

```bash
# Build frontend
cd frontend && npm run build

# Run backend (serves static files)
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/metrics` | GET | Application metrics |
| `/chat` | POST | Chat (non-streaming) |
| `/chat/stream` | GET | Chat with SSE streaming |

## Project Structure

```
.
├── app/                    # Backend
│   ├── agent/              # LLM agent and prompts
│   ├── llm/                # LLM providers
│   ├── models/             # Pydantic schemas
│   ├── observability/      # Langfuse integration
│   ├── config.py           # Configuration
│   └── main.py             # FastAPI app
├── frontend/               # React frontend
│   └── src/
│       ├── components/     # UI components
│       ├── hooks/          # Custom hooks (SSE, TTS)
│       └── utils/          # Utilities
├── scripts/                # Utility scripts
└── static/                 # Static files (TTS models)
```

## Testing

```bash
# Run backend tests
uv run pytest

# Run frontend build check
cd frontend && npm run build

# Lint frontend
cd frontend && npm run lint
```
