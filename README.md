# kSuite Documentation Assistant

AI-powered assistant for Infomaniak kSuite documentation (kDrive, kMeet, kChat). Built with a rigorous evaluation-driven approach to optimize each RAG pipeline component.

## Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenRouter API key ([get one here](https://openrouter.ai/keys))

### Run the App

```bash
# 1. Clone and configure
git clone <repo-url>
cd infomaniak-doc-assistant
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY

# 2. Start Qdrant and ingest documentation
docker compose up -d qdrant
docker compose -f docker-compose.eval.yml run --rm eval \
  python scripts/ingest_hybrid.py --recreate

# 3. Start the full stack
docker compose up -d

# 4. Open the app
open http://localhost:5173
```

### Run Evaluations

```bash
# Start Qdrant
docker compose up -d qdrant

# Run evaluation with specific model
docker compose -f docker-compose.eval.yml run --rm eval \
  python scripts/evaluate.py \
    --collection infomaniak_hybrid_full_doc_no_images \
    --hybrid-collection \
    --retrieval-mode hybrid \
    --model mistralai/mistral-nemo \
    --max-questions 27

# Results saved to data/evaluations/
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   RAG Pipeline v2                           │
├─────────────────────────────────────────────────────────────┤
│  DATA LAYER                                                 │
│  ├── Dataset:     cleaned_no_images (127 docs)              │
│  ├── Chunking:    full_document (no splitting)              │
│  └── Collection:  infomaniak_hybrid_full_doc_no_images      │
├─────────────────────────────────────────────────────────────┤
│  RETRIEVAL LAYER                                            │
│  ├── Dense:       Qwen3-Embedding-4B (2560 dims)            │
│  ├── Sparse:      Qdrant/bm25 with normalization            │
│  ├── Fusion:      Reciprocal Rank Fusion (k=60)             │
│  └── Top-K:       5 documents                               │
├─────────────────────────────────────────────────────────────┤
│  GENERATION LAYER                                           │
│  ├── Primary:     mistralai/mistral-nemo (12B)              │
│  └── Judge:       google/gemini-3-flash-preview             │
└─────────────────────────────────────────────────────────────┘
```

## Methodology

Every component was selected through rigorous A/B testing against 27 evaluation questions. Key decisions:

| Component | Decision | Reasoning |
|-----------|----------|-----------|
| Data | `cleaned_no_images` | -12% chunk size, cleaner text |
| Chunking | `full_document` | FAQs are atomic units; splitting breaks coherence |
| Retrieval | Normalized BM25 Hybrid | +9.9% correctness over dense-only |
| LLM | Mistral Nemo | 113x cheaper than flagship, 83% quality |

**Performance:** 76.5% correctness, 80.0% relevance, ~2.8s latency, ~$0.00009/query

See [docs/methodology.md](docs/methodology.md) for the complete evaluation framework and [docs/evaluations/](docs/evaluations/) for detailed reports.

## Project Structure

```
.
├── backend/
│   └── app/
│       ├── api/           # FastAPI endpoints
│       ├── core/          # Configuration
│       ├── rag/           # RAG components (retriever, generator, chunking)
│       └── evaluation/    # Evaluation framework
├── frontend/              # React + Vite chat interface
├── scripts/               # Ingestion and evaluation scripts
├── data/
│   ├── cleaned_no_images/ # Processed documentation
│   └── evaluations/       # Evaluation results (JSON)
├── docs/
│   ├── methodology.md     # Approach overview
│   └── evaluations/       # Detailed evaluation reports
├── docker-compose.yml     # Full stack (qdrant + backend + frontend)
└── docker-compose.eval.yml # Evaluation mode
```

## Model Providers

This project uses **OpenRouter** as the primary LLM provider. All evaluations were conducted with OpenRouter models to ensure reproducibility.

| Component | Model | Provider | Local Alternative |
|-----------|-------|----------|-------------------|
| Embeddings | qwen3-embedding-4b | OpenRouter | nomic-embed-text (Ollama) |
| Generation | mistral-nemo (12B) | OpenRouter | mistral:7b (Ollama) |
| Fallback | mistral-large (123B) | OpenRouter | None (too large) |
| Judge | gemini-flash | OpenRouter | None (closed model) |

**Why OpenRouter?**
- Access to open-weight models (Mistral, Qwen) via unified API
- Consistent evaluation metrics across runs
- No local GPU requirements
- Cost-effective (~$0.00009/query)

**Ollama support** exists for embeddings but wasn't used for evaluations. Running locally would require re-evaluation to validate quality metrics.

## Configuration

Key environment variables (see `.env.example` for all options):

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | **Required** - API key for LLM | - |
| `GENERATION_MODEL` | Model for answer generation | `mistralai/mistral-nemo` |
| `FALLBACK_MODEL` | Flagship model for complex queries | `mistralai/mistral-large` |
| `QDRANT_HOST` | Qdrant connection URL | `http://localhost:6333` |

## Local Development

For development without Docker:

```bash
# Install dependencies
uv sync
cd frontend && npm install && cd ..

# Start Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# Ingest documentation
uv run python scripts/ingest_hybrid.py --recreate

# Run backend
uv run uvicorn backend.app.main:app --reload

# Run frontend (separate terminal)
cd frontend && npm run dev
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/chat` | POST | Chat with streaming (Vercel AI SDK protocol) |
| `/api/collections` | GET | List indexed collections |

## Testing

```bash
# Backend tests
uv run pytest

# Frontend type check and lint
cd frontend && npm run build && npm run lint
```

## License

MIT
