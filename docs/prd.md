# Product Requirements Document
## Infomaniak Documentation AI Assistant

**Author:** Johann Taberlet  
**Date:** January 15, 2026  
**Version:** 1.0  
**Status:** Draft

---

## 1. Executive Summary

This project demonstrates a production-ready AI assistant that answers questions about Infomaniak's products and documentation. Built using Infomaniak's exact tech stack (LangChain, FastAPI, Qdrant, open-source LLMs), it showcases practical AI engineering skills for the AI Engineer position.

**Goal:** Prove hands-on experience with agent orchestration, RAG, and LLM serving in a concrete, relevant use case.

---

## 2. Problem Statement

Infomaniak develops AI features for kChat, kMeet, and kDrive. They need engineers who can:

- Design and develop AI agents with LangChain/Pydantic-AI
- Implement RAG pipelines for knowledge retrieval
- Optimize for latency, cost, and accuracy
- Deploy and monitor agents in production

**This demo directly addresses these requirements** by building a functional assistant that could realistically be integrated into Infomaniak's products.

---

## 3. Target Stack Alignment

| Infomaniak Requirement | Demo Implementation |
|------------------------|---------------------|
| LangChain | ✅ Agent orchestration |
| Pydantic-AI | ✅ Structured outputs & validation |
| RAG | ✅ Documentation retrieval |
| Qdrant | ✅ Vector storage |
| FastAPI | ✅ API layer |
| LLMs open source (Llama, Mistral, Qwen) | ✅ Via Ollama |
| Docker | ✅ Containerized deployment |
| Langfuse | ✅ Observability & tracing |

---

## 4. Functional Requirements

### 4.1 Core Features

**F1 - Documentation Ingestion**
- Scrape and process Infomaniak's public documentation (docs.infomaniak.com)
- Chunk documents intelligently (semantic splitting)
- Generate embeddings and store in Qdrant
- Support incremental updates

**F2 - Question Answering Agent**
- Accept natural language questions about Infomaniak products
- Retrieve relevant documentation chunks via RAG
- Generate accurate, sourced answers
- Handle follow-up questions (conversation memory)

**F3 - Multi-tool Agent**
- Primary tool: Documentation search (RAG)
- Secondary tool: Product comparison (structured data)
- Fallback: Acknowledge when information is not available

**F4 - API Endpoints**
```
POST /chat          - Send message, get response
GET  /health        - Service health check
GET  /metrics       - Performance metrics
```

### 4.2 Product Coverage

Initial scope - Infomaniak's main products:
- kDrive (cloud storage)
- kMeet (video conferencing)
- kChat (messaging)
- Mail Service
- Web Hosting

---

## 5. Non-Functional Requirements

### 5.1 Performance

| Metric | Target |
|--------|--------|
| Response latency (P95) | < 3 seconds |
| Retrieval accuracy | > 80% relevant chunks |
| Concurrent users | 10+ simultaneous |

### 5.2 Observability

- Request/response logging via Langfuse
- Token usage tracking
- Latency breakdown (embedding, retrieval, generation)
- Error rate monitoring

### 5.3 Reliability

- Graceful degradation when LLM unavailable
- Retry logic with exponential backoff
- Input validation and sanitization

---

## 6. Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT                                │
│                    (Web UI / cURL)                          │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI                                  │
│              (API Layer + Validation)                        │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   /chat     │  │  /health    │  │  /metrics   │         │
│  └──────┬──────┘  └─────────────┘  └─────────────┘         │
└─────────┼───────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                   LangChain Agent                            │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Agent Executor                      │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐       │   │
│  │  │ RAG Tool  │  │ Compare   │  │  Memory   │       │   │
│  │  │           │  │   Tool    │  │           │       │   │
│  │  └─────┬─────┘  └───────────┘  └───────────┘       │   │
│  └────────┼─────────────────────────────────────────────┘   │
└───────────┼─────────────────────────────────────────────────┘
            │
     ┌──────┴──────┐
     ▼             ▼
┌─────────┐  ┌─────────────┐
│ Qdrant  │  │   Ollama    │
│ (Vector │  │   (LLM)     │
│   DB)   │  │ Qwen/Mistral│
└─────────┘  └─────────────┘
```

---

## 7. Data Pipeline

### 7.1 Ingestion Flow

```
docs.infomaniak.com
        │
        ▼ (scraping)
┌───────────────┐
│  Raw HTML     │
└───────┬───────┘
        │
        ▼ (parsing)
┌───────────────┐
│  Clean Text   │
│  + Metadata   │
└───────┬───────┘
        │
        ▼ (chunking)
┌───────────────┐
│   Chunks      │
│  (~500 tokens)│
└───────┬───────┘
        │
        ▼ (embedding)
┌───────────────┐
│   Vectors     │
│  (Ollama)     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    Qdrant     │
└───────────────┘
```

### 7.2 Query Flow

```
User Question
      │
      ▼
┌─────────────┐
│  Embedding  │ ──────────────────┐
└──────┬──────┘                   │
       │                          │
       ▼                          ▼
┌─────────────┐           ┌─────────────┐
│   Qdrant    │           │   Langfuse  │
│  Similarity │           │   (Trace)   │
│   Search    │           └─────────────┘
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Top-K      │
│  Chunks     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Prompt    │
│  Assembly   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    LLM      │
│ Generation  │
└──────┬──────┘
       │
       ▼
   Response
```

---

## 8. Project Structure

```
infomaniak-docs-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Environment configuration
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── executor.py      # LangChain agent setup
│   │   ├── tools.py         # RAG and comparison tools
│   │   └── prompts.py       # System prompts
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py    # Embedding generation
│   │   ├── retriever.py     # Qdrant retrieval
│   │   └── chunker.py       # Document chunking
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   └── observability/
│       ├── __init__.py
│       └── langfuse.py      # Tracing setup
├── scripts/
│   ├── ingest.py            # Documentation scraper
│   └── seed_db.py           # Initial data load
├── tests/
│   ├── test_agent.py
│   ├── test_rag.py
│   └── test_api.py
├── docker-compose.yml       # Ollama + Qdrant + App
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## 9. Implementation Phases

### Phase 1: Foundation (Day 1)
- [ ] Project setup (Docker, dependencies)
- [ ] Qdrant container running
- [ ] Ollama with Qwen2.5 or Mistral
- [ ] Basic FastAPI skeleton
- [ ] Health check endpoint

### Phase 2: RAG Pipeline (Day 1-2)
- [ ] Documentation scraper (BeautifulSoup/Scrapy)
- [ ] Chunking strategy implementation
- [ ] Embedding generation (Ollama embeddings)
- [ ] Qdrant indexing
- [ ] Basic retrieval testing

### Phase 3: Agent Development (Day 2)
- [ ] LangChain agent setup
- [ ] RAG tool integration
- [ ] Prompt engineering
- [ ] Conversation memory
- [ ] Pydantic output validation

### Phase 4: Observability & Polish (Day 3)
- [ ] Langfuse integration
- [ ] Error handling
- [ ] Input sanitization
- [ ] Performance optimization
- [ ] Documentation (README)

### Phase 5: Demo & Deployment (Day 3)
- [ ] Simple web UI (optional)
- [ ] Docker Compose finalization
- [ ] GitHub repository
- [ ] Demo video/GIF

---

## 10. Key Technical Decisions

### 10.1 LLM Selection

**Primary: Qwen2.5-7B or Mistral-7B**
- Reasoning: Good balance of quality/speed for RAG tasks
- Fallback: Llama3.2-3B for faster responses

### 10.2 Embedding Model

**nomic-embed-text via Ollama**
- Reasoning: High quality, runs locally, no API costs

### 10.3 Chunking Strategy

**Semantic chunking with overlap**
- Chunk size: ~500 tokens
- Overlap: 50 tokens
- Split on: Headings, paragraphs

### 10.4 Retrieval Parameters

- Top-K: 5 chunks
- Similarity threshold: 0.7
- Reranking: Optional (if time permits)

---

## 11. Sample Interactions

**Example 1: Product Question**
```
User: Comment partager un dossier sur kDrive ?
Assistant: Pour partager un dossier sur kDrive, voici les étapes :

1. Ouvrez kDrive et sélectionnez le dossier
2. Cliquez sur "Partager" dans le menu contextuel
3. Ajoutez les adresses email des personnes
4. Définissez les permissions (lecture, édition)

[Source: Documentation kDrive - Partage de fichiers]
```

**Example 2: Comparison**
```
User: Quelle est la différence entre kMeet et kChat ?

Assistant: kMeet et kChat sont deux produits complémentaires :

**kChat** est une messagerie instantanée pour :
- Conversations texte en temps réel
- Partage de fichiers rapide
- Discussions de groupe

**kMeet** est une solution de visioconférence pour :
- Réunions vidéo
- Partage d écran
- Webinaires

En résumé : kChat pour le texte quotidien, kMeet pour les réunions vidéo.
```

**Example 3: Unavailable Information**
```
User: Quel est le prix de kDrive Enterprise ?

Assistant: Je n ai pas trouvé d information sur les tarifs Enterprise dans la documentation. Je vous recommande de contacter directement Infomaniak pour obtenir un devis personnalisé : https://www.infomaniak.com/contact
```

---

## 12. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Documentation structure changes | Medium | High | Robust scraper with fallbacks |
| LLM hallucinations | Medium | High | RAG-only responses, source citations |
| Performance issues | Low | Medium | Caching, async processing |
| Rate limiting (scraping) | Low | Low | Respectful crawling, local cache |

---

## 13. Success Metrics

**Demo Objectives:**
- [ ] Working chat interface
- [ ] Accurate answers to 10+ test questions
- [ ] Response time < 3s
- [ ] Clean, documented codebase
- [ ] Docker one-command startup

**Stretch Goals:**
- [ ] Langfuse dashboard with traces
- [ ] Simple web UI
- [ ] Benchmark comparison (Qwen vs Mistral)

---

## 14. Dependencies

### Python Packages
```
langchain>=0.1.0
langchain-community>=0.0.10
pydantic>=2.0
fastapi>=0.109.0
uvicorn>=0.27.0
qdrant-client>=1.7.0
beautifulsoup4>=4.12.0
requests>=2.31.0
langfuse>=2.0.0
python-dotenv>=1.0.0
```

### External Services
- Ollama (local LLM serving)
- Qdrant (vector database)
- Langfuse (optional, observability)

---

## 15. Open Questions

1. **Bilingual support?** Should the assistant respond in French/English based on query language?
2. **Streaming?** Should responses stream for better UX?
3. **UI scope?** Minimal CLI, or basic web interface?
4. **Caching strategy?** Cache embeddings, responses, or both?

---

## Appendix A: Sample docker-compose.yml

```yaml
version: "3.8"

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - QDRANT_HOST=http://qdrant:6333
    depends_on:
      - ollama
      - qdrant

volumes:
  ollama_data:
  qdrant_data:
```

---

## Appendix B: Sample Prompt Template

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

---

*Document generated for Johann Taberlet - AI Engineer Application - Infomaniak*