# kSuite Assistant - Claude Code Context

## Project Status: v2 Rewrite in Progress

**Branch**: `v2` (fresh start, documented approach)
**Goal**: Demo for Infomaniak recruitment showcasing AI engineering excellence

## What We're Building

1. **Phase 1**: RAG chatbot for kSuite documentation (kDrive, kMeet, kChat)
2. **Phase 2**: Agentic system with simulated kSuite apps (reactive UI)

## Key Documents

- **PROJECT_ROADMAP.md**: Full roadmap with phases, architecture, evaluation strategy
- **docs/decisions/**: Architecture Decision Records (ADRs)
- **docs/evaluations/**: Benchmark results

## Technical Decisions Made

### Frontend
- **Vercel AI SDK** for streaming + tool calling (works with Vite React)
- **json-render** for constrained generative UI components
- No RSC (not available in Vite)

### Backend
- **FastAPI** with Vercel AI SDK stream protocol
- **Qdrant** for vector storage (Docker, not cloud)
- **Langfuse** for observability everywhere

### Models (Open Source Priority)
- **LLM**: Qwen3-8B (primary), consider GLM-4-9B-0414
- **Embeddings**: Qwen3-Embedding-4B
- **Providers**: Ollama (local), OpenRouter (cloud), Vertex AI (optional)

## Research Still Needed

1. **Langfuse integration patterns** for RAG + agents
2. **CopilotKit vs Vercel AI SDK** detailed comparison for agentic UI
3. **GLM-4-9B-0414** benchmark for tool calling
4. **Optimal chunking strategy** for FAQ documentation

## Current State

- Raw scraped docs exist in `data/`
- v1 code exists but needs complete rewrite
- v2 branch created, ready for fresh implementation

## Guiding Principles

1. **Document everything**: ADRs for all decisions
2. **Evaluate everything**: Benchmarks at each step
3. **Error handling**: Zero unhandled exceptions
4. **Security**: Input validation, output guardrails
5. **Reproducibility**: Docker one-command setup
6. **Professional README**: Show methodology, not just code

## Development Tools

- Use `pyright` for Python type checking
- Use `npm run lint` for frontend linting
- Run `uv run pytest` for backend tests

## Code Conventions

### Python (Backend)
- Use type hints for all function signatures
- Follow PEP 8 style guide
- Use `pydantic` for data validation
- Configuration via environment variables

### TypeScript (Frontend)
- Strict TypeScript mode enabled
- Use functional components with hooks
- Export types from dedicated `types.ts` files

## Commands

```bash
# Start infrastructure
docker-compose up -d

# Run evaluations
uv run python scripts/evaluate.py

# Development
uv run uvicorn app.main:app --reload
cd frontend && npm run dev

# Tests
uv run pytest
cd frontend && npm run build && npm run lint
```

## Next Steps

1. Clear v2 branch (preserve raw data only)
2. Set up new project structure
3. Run research tasks (Langfuse, CopilotKit, GLM-4)
4. Implement data cleaning + chunking with evaluation
5. Continue per PROJECT_ROADMAP.md

## Star Wars Experiment Reference

The `/Users/jo/dev/perso/Star-Wars-Movie-Expert` project contains:
- Working evaluation framework (can be adapted)
- Model provider abstraction (Ollama/OpenRouter)
- Embedding comparison methodology

Key learnings:
- Embedding models work well, LLM is usually the bottleneck
- Relevance + Faithfulness + Correctness metrics are effective
- OpenRouter works with `check_embedding_ctx_length=False`
