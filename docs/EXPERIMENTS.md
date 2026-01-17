# RAG Architecture Experiments

This document summarizes the experiments conducted to develop and optimize the RAG (Retrieval-Augmented Generation) architecture for the Infomaniak Documentation Assistant.

## Overview

We evaluated multiple configurations across three key dimensions:
1. **Chunking strategies** - How to split documents for embedding
2. **Embedding models** - Which models produce the best semantic representations
3. **LLM models** - Which models generate the most accurate responses

Each configuration was tested against a standardized evaluation set of 20 questions covering kDrive, kMeet, and kChat products.

---

## Evaluation Methodology

### Test Dataset
- **20 carefully crafted questions** spanning all three products
- Each question includes a "perfect answer" with key points to verify
- Questions range from simple ("How do I create a kMeet meeting?") to complex ("How do I sync kDrive with a Synology NAS?")

### Scoring System
| Rating | Score | Description |
|--------|-------|-------------|
| Complete | 3 | All key points covered (≥80% coverage) |
| Partial | 2 | Most key points covered (50-79% coverage) |
| Minimal | 1 | Few key points covered (<50% coverage) |
| Wrong | 0 | Incorrect or no relevant information |

### Metrics
- **Total Score**: Sum of all ratings (max 60)
- **Coverage**: Percentage of expected key points found in response
- **Response Time**: Time to generate complete answer

---

## Experiment 1: Pure Vector Search (Baseline)

### Configuration
- **Chunking**: Split documents into 1500-char chunks with 200-char overlap
- **Embedding**: `qwen/qwen3-embedding-8b` (4096 dimensions)
- **Search**: Pure vector similarity (cosine distance)
- **LLM**: `mistralai/ministral-8b`

### Results
| Metric | Value |
|--------|-------|
| Success Rate | ~52% |
| Correct | ~30% |
| Wrong | ~48% |

### Key Issues
- **Proper nouns failed completely**: "Euria" (AI assistant) and "Drop Box" (kDrive feature) returned 0% accuracy
- Semantic search couldn't match exact terms that weren't in training data
- Technical terms like "WebDAV" had inconsistent retrieval

---

## Experiment 2: Hybrid Search (BM25 + Vector)

### Configuration
- **Chunking**: Same as baseline (1500-char chunks)
- **Embedding**: `qwen/qwen3-embedding-8b` (4096 dimensions)
- **Search**: Hybrid - BM25 keyword matching + vector similarity
- **Fusion**: Reciprocal Rank Fusion (RRF) with k=60
- **LLM**: `mistralai/ministral-8b`

### Results
| Metric | Value | Change |
|--------|-------|--------|
| Success Rate | 90% | **+38%** |
| Correct | 50% | +20% |
| Wrong | 10% | -38% |

### Key Improvements
- **Euria question**: 0% → Correctly identified as AI assistant
- **Drop Box question**: 0% → Partially correct with creation steps
- BM25 captures exact keyword matches that semantic search misses

### Implementation
```python
# Reciprocal Rank Fusion combines rankings
rrf_score = sum(1 / (k + rank)) for each retriever
```

---

## Experiment 3: Chunking Strategies

We compared two chunking approaches:

### A) Split Strategy (V1)
- Documents split into 1500-char chunks with overlap
- 128 documents → 387 chunks
- Better for long documents with multiple topics

### B) Document Strategy (V2)
- Entire FAQ kept as single chunk
- 128 documents → 128 chunks
- Better for focused, single-topic documents

### Results Comparison

| Strategy | Total Score | Complete | Minimal | Wrong |
|----------|-------------|----------|---------|-------|
| Split (V1) | 52/60 (86.7%) | 65% | 5% | 0% |
| Document (V2) | 49/60 (81.7%) | 55% | 10% | 0% |

**Conclusion**: Split strategy performed slightly better overall, chosen as default.

---

## Experiment 4: Embedding Models

### Models Tested

| Model | Dimensions | Provider |
|-------|------------|----------|
| `qwen/qwen3-embedding-8b` | 4096 | OpenRouter |
| `baai/bge-m3` | 1024 | OpenRouter |
| `nomic-embed-text` | 768 | Ollama (local) |

### Results

**Qwen3 Embedding (4096d)** - Best overall performance
- Better semantic understanding
- Handles multilingual content (French documentation)
- Higher dimensionality captures more nuance

**BGE-M3 (1024d)** - Good alternative
- Faster inference
- Smaller storage footprint
- Slightly lower accuracy on complex queries

**Selected**: `qwen/qwen3-embedding-8b` for production

---

## Experiment 5: LLM Models

### Models Tested

| Model | Provider | Response Time |
|-------|----------|---------------|
| `mistralai/ministral-8b` | OpenRouter | ~11s |
| `mistralai/mistral-large-latest` | Mistral API | ~24s |
| `google/gemini-flash-2.0` | OpenRouter | ~15s |
| `qwen/qwen3-max` | Qwen API | ~18s |

### Results

| Model | Score | Coverage | Analysis |
|-------|-------|----------|----------|
| **Mistral Large** | 60/60 (100%) | 98% | Perfect accuracy, slower |
| Gemini Flash 2.0 | 56/60 (93%) | 91% | Fast, occasional gaps |
| Qwen3 Max | 54/60 (90%) | 89% | Good multilingual |
| Ministral 8B | 50/60 (83%) | 80% | Fast but misses details |

### Key Findings

**Mistral Large** achieved perfect scores:
- 100% of questions rated "Complete"
- 98% average coverage of key points
- Best at following complex multi-step instructions
- Worth the latency trade-off for accuracy

**Selected**: `mistral-large-latest` for production

---

## Final Architecture

Based on all experiments, the selected production configuration:

```python
# RAG Configuration
RAG_CHUNK_SIZE = 1500
RAG_CHUNK_OVERLAP = 200
RAG_TOP_K = 15  # Increased from 10 for better coverage
RAG_HYBRID_ENABLED = True
RAG_BM25_K = 60  # RRF fusion constant

# Models
EMBEDDING_MODEL = "qwen/qwen3-embedding-8b"  # 4096 dimensions
CHAT_MODEL = "mistral-large-latest"

# Vector Store
QDRANT_COLLECTION = "infomaniak_docs"
```

### Architecture Diagram

```
User Query
    │
    ├─────────────────────────────────┐
    │                                 │
    ▼                                 ▼
┌─────────────┐                 ┌─────────────┐
│   Vector    │                 │    BM25     │
│   Search    │                 │   Search    │
│ (Semantic)  │                 │ (Keyword)   │
└─────┬───────┘                 └─────┬───────┘
      │                               │
      └───────────┬───────────────────┘
                  │
                  ▼
         ┌───────────────┐
         │ Reciprocal    │
         │ Rank Fusion   │
         └───────┬───────┘
                 │
                 ▼
         ┌───────────────┐
         │  Top K (15)   │
         │  Documents    │
         └───────┬───────┘
                 │
                 ▼
         ┌───────────────┐
         │ Mistral Large │
         │   (ReAct)     │
         └───────┬───────┘
                 │
                 ▼
           Response
```

---

## Performance Summary

| Metric | Baseline | Final | Improvement |
|--------|----------|-------|-------------|
| Success Rate | 52% | 100% | **+48%** |
| Complete Answers | 30% | 100% | **+70%** |
| Wrong Answers | 48% | 0% | **-48%** |
| Avg Coverage | ~60% | 98% | **+38%** |

---

## Future Improvements

1. **Query Expansion**: Automatically expand queries with synonyms (e.g., "livestream" → "live streaming")
2. **Contextual Embeddings**: Add document context to chunk embeddings
3. **Reranking**: Add cross-encoder reranking for final result refinement
4. **Caching**: Cache frequent queries for faster response times

---

## Evaluation Files

The raw evaluation data is stored in `tests/evaluation/`:
- `manual_test_questions.json` - Test dataset with expected answers
- `*_responses.json` - Raw responses from each model/configuration
- `*_report.md` - Detailed analysis reports
- `comparison_report.md` - Final comparison across all tests
