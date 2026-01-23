# kSuite Assistant - Project Roadmap v2

> **Purpose**: AI-powered documentation assistant for Infomaniak kSuite (kDrive, kMeet, kChat)
> **Target**: Demo for Infomaniak recruitment showcasing AI engineering excellence
> **Timeline**: Weekend sprint (Jan 24-26, 2026)

---

## Table of Contents

1. [Project Vision](#1-project-vision)
2. [Architecture Principles](#2-architecture-principles)
3. [Tech Stack Decisions](#3-tech-stack-decisions)
4. [Roadmap Phases](#4-roadmap-phases)
5. [Evaluation Strategy](#5-evaluation-strategy)
6. [Documentation Requirements](#6-documentation-requirements)
7. [Research Tasks](#7-research-tasks)

---

## 1. Project Vision

### What We're Building

**Phase 1 - RAG Chatbot**
- Documentation Q&A for kDrive, kMeet, kChat
- Professional UI with streaming responses
- Generative UI components (step guides, platform availability)

**Phase 2 - Agentic System**
- LLM agents that interact with simulated kSuite apps
- User: "Create a meeting with John and David at 3pm"
- Agent: Searches contacts → Opens kMeet → Creates meeting → Sends invites
- Reactive UI showing agent actions in real-time

### Success Criteria

| Criteria | Metric |
|----------|--------|
| RAG Quality | >80% correctness on eval dataset |
| Response Latency | <3s p95 for simple queries |
| Error Handling | Zero unhandled exceptions |
| Documentation | Complete ADRs for all decisions |
| Reproducibility | One-command Docker setup |

---

## 2. Architecture Principles

### 2.1 Separation of Concerns

```
backend/
├── app/
│   ├── api/              # FastAPI routes (thin layer)
│   ├── core/             # Config, security, error handling
│   ├── rag/              # RAG pipeline (retrieval, generation)
│   │   ├── chunking/     # Chunking strategies
│   │   ├── embeddings/   # Embedding providers
│   │   ├── retrieval/    # Vector + BM25 hybrid
│   │   └── generation/   # LLM response generation
│   ├── agents/           # Agentic system
│   │   ├── tools/        # Tool definitions
│   │   ├── executor/     # Agent orchestration
│   │   └── state/        # Agent state management
│   ├── llm/              # LLM provider abstraction
│   │   ├── base.py       # Abstract interface
│   │   ├── ollama.py     # Local Ollama
│   │   ├── openrouter.py # OpenRouter API
│   │   └── vertex.py     # Google Vertex AI (optional)
│   └── observability/    # Langfuse + metrics
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evaluation/       # RAG quality tests
└── scripts/
    ├── ingest.py         # Data ingestion
    ├── evaluate.py       # Run evaluations
    └── benchmark.py      # Model benchmarking

frontend/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── chat/         # Chat interface
│   │   ├── generative/   # json-render components
│   │   └── simulation/   # Fake kSuite UIs
│   ├── hooks/            # Custom hooks (useChat, etc.)
│   ├── stores/           # State management
│   └── lib/              # Utilities
```

### 2.2 Provider Abstraction

All LLM/embedding providers must implement a common interface:

```python
class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: list[Message], **kwargs) -> AsyncIterator[str]: ...

    @abstractmethod
    async def generate_with_tools(self, messages: list[Message], tools: list[Tool]) -> ToolResponse: ...

class EmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]: ...
```

### 2.3 Error Handling Strategy

```python
# Hierarchical exception classes
class KSuiteError(Exception): ...
class RAGError(KSuiteError): ...
class RetrievalError(RAGError): ...
class GenerationError(RAGError): ...
class ProviderError(KSuiteError): ...
class RateLimitError(ProviderError): ...

# Global error handler with Langfuse tracking
@app.exception_handler(KSuiteError)
async def ksuite_error_handler(request, exc):
    langfuse.capture_exception(exc)
    return JSONResponse(status_code=exc.status_code, content={"error": exc.message})
```

### 2.4 Security & Guardrails

- **Input validation**: Pydantic schemas for all inputs
- **Output validation**: Ensure LLM responses match expected format
- **Prompt injection defense**: Input sanitization + system prompt hardening
- **Rate limiting**: Per-user rate limits
- **Content filtering**: Block harmful outputs

---

## 3. Tech Stack Decisions

### 3.1 Models (Open Source Priority)

| Task | Primary Model | Fallback | Rationale |
|------|--------------|----------|-----------|
| **Chat/RAG** | Qwen3-8B | Qwen3-14B | Best open-source balance |
| **Embeddings** | Qwen3-Embedding-4B | nomic-embed-text | High quality, reasonable size |
| **Judge (Eval)** | Gemini 2 Flash | Qwen3-32B | Cost-effective evaluation |
| **Agentic** | GLM-4-9B-0414 or Qwen3-14B | - | Tool calling capability |

**Note**: GLM-4-9B-0414 (just released) claims state-of-the-art for its size - needs benchmarking.

### 3.2 Infrastructure

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Vector DB** | Qdrant | Self-hosted, hybrid search |
| **Backend** | FastAPI | Async, type-safe, OpenAPI |
| **Frontend** | Vite + React + TypeScript | Fast dev, modern tooling |
| **Streaming** | Vercel AI SDK | Production-ready hooks |
| **Generative UI** | json-render | Constrained components |
| **Observability** | Langfuse | LLM-native tracing |
| **Containerization** | Docker Compose | One-command setup |

### 3.3 Providers Configuration

```yaml
# .env.example
LLM_PROVIDER=openrouter  # ollama | openrouter | vertex

# Ollama (local)
OLLAMA_BASE_URL=http://localhost:11434

# OpenRouter (cloud)
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_CHAT_MODEL=qwen/qwen3-8b
OPENROUTER_EMBEDDING_MODEL=qwen/qwen3-embedding-4b

# Vertex AI (optional)
GOOGLE_PROJECT_ID=...
VERTEX_LOCATION=us-central1

# Langfuse
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

## 4. Roadmap Phases

### Phase 0: Project Setup (2h)
- [ ] Clear v2 branch, preserve raw data only
- [ ] Set up project structure (backend/frontend/docs)
- [ ] Docker Compose for Qdrant + Ollama
- [ ] Configure Langfuse project
- [ ] Create CLAUDE.md with project context

### Phase 1: Data Pipeline (3h)
- [ ] **Research**: Optimal chunking strategies for FAQ docs
- [ ] **Implement**: Data cleaning pipeline
  - Strip irrelevant content (headers, footers, navigation)
  - Preserve structure (headings, lists, code blocks)
  - Extract metadata (product, category, language)
- [ ] **Implement**: Chunking with multiple strategies
  - Recursive character splitting
  - Semantic chunking (by heading/section)
  - Sentence-window chunking
- [ ] **Evaluate**: Compare chunking strategies with retrieval metrics
- [ ] **Document**: ADR for chunking decision

### Phase 2: RAG Core (4h)
- [ ] **Implement**: Embedding provider abstraction
- [ ] **Implement**: Hybrid retrieval (dense + BM25)
- [ ] **Implement**: Reranking (optional, if needed)
- [ ] **Implement**: Query expansion/reformulation
- [ ] **Create**: Evaluation dataset (50+ questions)
- [ ] **Evaluate**: End-to-end RAG quality
  - Correctness (LLM-as-judge)
  - Faithfulness (grounded in context)
  - Relevance (context quality)
  - Latency (retrieval + generation)
- [ ] **Optimize**: Based on evaluation results
- [ ] **Document**: ADR for RAG architecture

### Phase 3: Backend API (3h)
- [ ] **Implement**: FastAPI application structure
- [ ] **Implement**: Vercel AI SDK stream protocol
- [ ] **Implement**: Error handling middleware
- [ ] **Implement**: Langfuse tracing integration
- [ ] **Implement**: Rate limiting
- [ ] **Write**: API tests
- [ ] **Document**: OpenAPI spec review

### Phase 4: Frontend Chat (4h)
- [ ] **Research**: CopilotKit vs Vercel AI SDK comparison
- [ ] **Implement**: Chat interface with useChat
- [ ] **Implement**: json-render components
  - StepGuide (numbered instructions)
  - PlatformAvailability (feature matrix)
  - CodeBlock (with copy)
  - ImagePreview (documentation screenshots)
- [ ] **Implement**: Streaming UX (typing indicator, auto-scroll)
- [ ] **Style**: Professional, clean design
- [ ] **Document**: Component catalog

### Phase 5: Agentic System (4h)
- [ ] **Design**: Tool definitions for kSuite actions
  - kMeet: createMeeting, inviteParticipant, startMeeting
  - kDrive: searchFiles, shareFile, createFolder
  - kChat: sendMessage, createChannel, searchContacts
- [ ] **Implement**: Simulated app state (React context/Zustand)
- [ ] **Implement**: Agent executor with tool calling
- [ ] **Implement**: Simulated UI components
  - Fake kMeet interface
  - Fake kDrive file browser
  - Fake kChat messaging
- [ ] **Implement**: Action visualization (show agent steps)
- [ ] **Test**: End-to-end agent scenarios
- [ ] **Document**: Agent architecture

### Phase 6: Polish & Documentation (3h)
- [ ] **Write**: Professional README
  - Project overview
  - Architecture diagram
  - Setup instructions (Docker)
  - Evaluation results
  - Design decisions summary
- [ ] **Create**: Demo video/GIF
- [ ] **Review**: All ADRs complete
- [ ] **Test**: Full Docker setup from scratch
- [ ] **Optimize**: Performance tuning

---

## 5. Evaluation Strategy

### 5.1 Evaluation Framework

```
evaluation/
├── datasets/
│   ├── rag_eval.yaml         # RAG quality questions
│   ├── agent_eval.yaml       # Agent scenario tests
│   └── edge_cases.yaml       # Adversarial inputs
├── judges/
│   ├── correctness.py        # Is answer correct?
│   ├── faithfulness.py       # Is answer grounded?
│   ├── relevance.py          # Is context relevant?
│   └── safety.py             # Is output safe?
├── runners/
│   ├── rag_runner.py         # RAG evaluation
│   ├── agent_runner.py       # Agent evaluation
│   └── benchmark_runner.py   # Model comparison
└── reports/
    └── {timestamp}_{model}.json
```

### 5.2 Evaluation Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Correctness** | Answer matches expected (LLM judge) | >80% |
| **Faithfulness** | Answer grounded in context | >90% |
| **Relevance** | Retrieved context is useful | >85% |
| **Latency P50** | Median response time | <2s |
| **Latency P95** | 95th percentile | <5s |
| **Error Rate** | Unhandled errors | <1% |

### 5.3 Continuous Evaluation

- Run evaluations after each significant change
- Track metrics in Langfuse
- Compare models systematically
- Document all results in `/docs/evaluations/`

---

## 6. Documentation Requirements

### 6.1 Architecture Decision Records (ADRs)

Location: `/docs/decisions/`

| ADR | Topic |
|-----|-------|
| 001 | Frontend SDK Selection |
| 002 | Chunking Strategy |
| 003 | RAG Architecture |
| 004 | Model Selection |
| 005 | Agent Framework |
| 006 | Observability Strategy |

### 6.2 README Structure

```markdown
# kSuite Documentation Assistant

## Overview
[What it does, why it matters]

## Demo
[GIF/Video showing the chatbot and agent in action]

## Architecture
[Diagram + explanation]

## Key Features
- RAG-based documentation Q&A
- Generative UI components
- Agentic system with simulated kSuite

## Quick Start
docker-compose up

## Configuration
[Provider setup, model selection]

## Evaluation Results
[Summary of benchmarks]

## Design Decisions
[Links to ADRs]

## Development
[How to contribute, run tests]
```

---

## 7. Research Tasks

### 7.1 Required Research (Before Implementation)

| Topic | Output | Priority |
|-------|--------|----------|
| **Langfuse Integration Patterns** | Best practices for tracing RAG + agents | High |
| **CopilotKit vs Vercel AI SDK** | Detailed comparison for agentic UI | High |
| **GLM-4-9B-0414 Capabilities** | Benchmark for tool calling | Medium |
| **Optimal Chunking for FAQ Docs** | Strategy recommendation | High |
| **Hybrid Search Tuning** | BM25 + dense weights | Medium |

### 7.2 Research Template

Each research task should produce:
1. **Summary**: Key findings (1 page)
2. **Comparison table**: If evaluating options
3. **Recommendation**: Clear decision
4. **Code example**: If applicable
5. **References**: Sources used

---

## 8. Success Checklist

### For Recruiter Review

- [ ] Professional README with clear value proposition
- [ ] One-command Docker setup that works
- [ ] Clean, well-structured codebase
- [ ] Comprehensive error handling
- [ ] Full observability with Langfuse
- [ ] Documented evaluation results
- [ ] ADRs showing engineering thinking
- [ ] Working demo (RAG + Agent)
- [ ] Test coverage for critical paths

### Technical Excellence Indicators

- [ ] Type safety throughout (Pydantic, TypeScript)
- [ ] Async where beneficial
- [ ] Proper abstraction layers
- [ ] No hardcoded values (all configurable)
- [ ] Security considerations addressed
- [ ] Performance optimized (right model sizes)
- [ ] Graceful degradation on errors

---

## Quick Reference

### Commands

```bash
# Full setup
docker-compose up -d

# Run evaluations
uv run python scripts/evaluate.py

# Development
uv run uvicorn app.main:app --reload
cd frontend && npm run dev
```

### Key Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Full stack setup |
| `.env.example` | Configuration template |
| `scripts/evaluate.py` | Run RAG evaluations |
| `docs/decisions/*.md` | Architecture decisions |
| `docs/evaluations/*.json` | Evaluation results |

---

*Last updated: 2026-01-23*
*Author: Johann Taberlet*
