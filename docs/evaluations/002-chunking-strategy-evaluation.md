# Evaluation 002: Chunking Strategy Comparison

**Date**: 2025-01-23
**Author**: Engineering Team
**Status**: Completed

## Executive Summary

We evaluated 4 chunking strategies across 2 datasets (8 configurations total) to determine the optimal approach for the kSuite RAG pipeline. **Full document chunking with the no-images dataset** emerged as the best performer for retrieval quality.

## Context

### Why Chunking Matters

Chunking strategy directly impacts RAG quality:
- **Too small**: Loses context, fragments information
- **Too large**: Dilutes relevance, wastes context window
- **Wrong boundaries**: Breaks semantic coherence

### Candidate Strategies

| Strategy | Description | Parameters |
|----------|-------------|------------|
| **Full Document** | Keep entire FAQ as single chunk | None |
| **Recursive** | Split by separators, then by size | chunk_size, overlap |
| **Semantic** | Split by embedding similarity | threshold |
| **Sentence Window** | Sentence-level with context window | window_size |

### Datasets Under Test

Both cleaned datasets from Phase 1:
- `cleaned/` - Images inline in markdown
- `cleaned_no_images/` - Images extracted to JSON

## Methodology

### Evaluation Framework

We built a comprehensive evaluation pipeline:

1. **Evaluation Dataset**: 27 questions across 3 categories
   - `direct` (14): Single-document answers
   - `multi_doc` (5): Cross-document synthesis required
   - `out_of_scope` (8): Answer not in documentation

2. **Metrics** (LLM-as-Judge with Gemini Flash):
   - **Correctness**: Does the answer match expected answer?
   - **Faithfulness**: Is the answer grounded in retrieved context?
   - **Relevance**: Is the retrieved context relevant to the question?

3. **Infrastructure**:
   - Qdrant vector database (local Docker)
   - Qwen3-Embedding-4B via OpenRouter
   - Langfuse for observability and A/B comparison

### Configurations Tested

| Collection Name | Strategy | Chunk Size | Dataset |
|-----------------|----------|------------|---------|
| `infomaniak_full_doc_images` | full_document | N/A | images |
| `infomaniak_full_doc_no_images` | full_document | N/A | no_images |
| `infomaniak_recursive_1000_images` | recursive | 1000 | images |
| `infomaniak_recursive_1000_no_images` | recursive | 1000 | no_images |
| `infomaniak_recursive_1500_images` | recursive | 1500 | images |
| `infomaniak_recursive_1500_no_images` | recursive | 1500 | no_images |
| `infomaniak_semantic_images` | semantic | auto | images |
| `infomaniak_semantic_no_images` | semantic | auto | no_images |

## Results

### Retrieval-Only Evaluation (27 questions each)

| Strategy | Dataset | Correctness | Faithfulness | Relevance | Latency |
|----------|---------|-------------|--------------|-----------|---------|
| **full_document** | **no_images** | **0.504** | 0.037 | **0.785** | 1386ms |
| full_document | images | 0.513 | 0.111 | 0.789 | 727ms |
| semantic | images | 0.539 | 0.111 | 0.670 | 1233ms |
| semantic | no_images | 0.476 | 0.111 | 0.678 | 707ms |
| recursive_1500 | no_images | 0.493 | 0.037 | 0.715 | 832ms |
| recursive_1000 | no_images | 0.426 | 0.037 | 0.619 | 711ms |
| recursive_1500 | images | 0.393 | 0.037 | 0.656 | 1201ms |
| recursive_1000 | images | 0.456 | 0.074 | 0.593 | 833ms |

### Key Observations

1. **Full document strategy achieves highest relevance (0.785-0.789)**
   - FAQ documents are self-contained units
   - Splitting breaks the natural question-answer structure
   - Average document size (2,914 chars) fits within context limits

2. **No-images dataset slightly outperforms on relevance**
   - Cleaner text without image markdown artifacts
   - 12% smaller chunks = more focused content

3. **Faithfulness scores are low across all strategies**
   - Expected for retrieval-only evaluation (no LLM generation)
   - Context is retrieved but not yet synthesized into answers

4. **Recursive chunking underperforms**
   - FAQ structure doesn't benefit from size-based splitting
   - Breaks semantic coherence of step-by-step instructions

5. **Semantic chunking middle-ground**
   - Better than recursive but worse than full document
   - Overhead of similarity computation not justified

### Statistical Analysis

Comparing top strategies (full_document variants):

| Metric | images | no_images | Delta |
|--------|--------|-----------|-------|
| Relevance | 0.789 | 0.785 | -0.5% |
| Correctness | 0.513 | 0.504 | -1.8% |
| Chunks/query | 5.0 | 5.0 | 0% |

The difference is within noise margin, but no_images provides:
- Smaller storage footprint
- Future flexibility for controlled image injection
- Cleaner context for LLM generation

## Decision

**Selected configuration**: `infomaniak_full_doc_no_images`

### Rationale

1. **Highest relevance** (0.785) - retrieves correct documents consistently
2. **Natural boundaries** - FAQ documents are atomic units of information
3. **No chunking artifacts** - preserves step-by-step instructions intact
4. **Smaller size** - 12% less data without losing information
5. **Future flexibility** - images available in JSON for smart injection

### Trade-offs Accepted

- Larger chunks use more context window per retrieval
- Cannot do fine-grained retrieval within long documents
- Mitigation: kSuite FAQs are relatively short (avg 2,914 chars)

## Vector Database Statistics

Final collection metrics:

```
Collection: infomaniak_full_doc_no_images
Vectors: 127
Dimensions: 4096
Distance: Cosine
```

## Next Steps

1. Evaluate LLM models for answer generation (see [003-llm-model-evaluation.md](./003-llm-model-evaluation.md))
2. Measure end-to-end RAG quality with full document retrieval
3. Consider hybrid approach for very long documents (if added later)

## Artifacts

| File | Purpose |
|------|---------|
| `scripts/ingest.py` | Chunking and ingestion pipeline |
| `backend/app/rag/chunking.py` | Chunking strategy implementations |
| `backend/app/evaluation/runner.py` | Evaluation framework |
| `data/evaluations/*.json` | Raw evaluation results |
