# Infomaniak Documentation AI Assistant

AI assistant for Infomaniak documentation (kDrive, kMeet, kChat, kSuite, SwissTransfer).

## Architecture

- **Backend**: FastAPI + LangChain with RAG (Retrieval Augmented Generation)
- **Frontend**: React + TypeScript + Vite
- **Vector Store**: Qdrant
- **LLM**: Ollama (local) or OpenRouter (cloud)

## Quick Start

```bash
# 1. Install dependencies
uv sync && cd frontend && npm install && cd ..

# 2. Configure environment
cp .env.example .env
# Edit .env: set LLM_PROVIDER and API keys

# 3. Start Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# 4. Ingest documentation into vector store
uv run python scripts/ingest.py

# 5. Run the application
uv run uvicorn app.main:app --reload  # Backend on :8000
cd frontend && npm run dev             # Frontend on :5173
```

## Configuration

Edit `.env` to switch between local (Ollama) and cloud (OpenRouter) LLM providers:

| Variable | Description |
|----------|-------------|
| `LLM_PROVIDER` | `ollama` or `openrouter` |
| `OPENROUTER_API_KEY` | Required for OpenRouter |
| `OPENROUTER_CHAT_MODEL` | e.g. `mistralai/mistral-large-2512` |
| `QDRANT_HOST` | Default: `http://localhost:6333` |

See `.env.example` for all available options.

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

## Known Limitations

### Model Compatibility

While the project supports local models via Ollama, **all testing has been done with Mistral Large 3 via OpenRouter**. Using smaller or less capable models may result in:

- Poorly structured responses that break the Generative UI components
- Incorrect NDJSON output format for streaming
- Reduced prompt adherence and instruction following

See the [Roadmap](#roadmap) section for planned prompt optimization work.

### Image Relevance in Responses

The assistant may occasionally display images that are not contextually accurate. This happens because:

- Images are scraped from Infomaniak FAQ pages and converted to markdown URLs
- During ingestion, images are **stripped from the content** to optimize text embeddings
- The LLM has no knowledge of what each image URL actually depicts
- When the model decides to include an image, it may select an incorrect one

See the [Roadmap](#roadmap) for planned improvements.

## Roadmap

### Multimodal RAG Enhancement

To improve image relevance in responses, the following improvements are planned:

1. **Vision-based captioning at ingestion**
   - Use Gemini 2.5 Flash Batch API to generate detailed descriptions of each screenshot
   - Extract UI elements (buttons, menus, dialogs) with their labels and purposes
   - Store captions as separate chunks linked to image URLs

2. **Structured metadata storage**
   - Store image descriptions with rich metadata in Qdrant
   - Include `image_url`, `caption`, `ui_elements`, and `surrounding_context`
   - Enable retrieval of relevant images based on semantic search

3. **URL validation at generation**
   - Cross-check image URLs in LLM responses against retrieved documents
   - Reject hallucinated URLs that weren't in the retrieval context

4. **Query classification for selective vision**
   - Classify queries as TEXT_ONLY, IMAGE_REQUIRED, or HYBRID
   - Only fetch raw images for visual queries to optimize costs

### Small Model Support

Optimize prompts for smaller/local models to ensure proper output structure:

1. **Prompt engineering for smaller models**
   - Simplify system prompts for better adherence on 7B-8B models
   - Add few-shot examples for NDJSON output format
   - Test and validate with Qwen3 8B, Mistral 7B, and similar models

2. **Structured output enforcement**
   - Ensure Generative UI components (`step_guide`, `platform_availability`) render correctly
   - Add fallback parsing for malformed JSON responses
   - Validate output schema before streaming to frontend
