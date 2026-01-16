# V1 Architecture Evaluation Results (Split Strategy)

**Date:** 2026-01-16
**Documents:** 128 (including 127 auto-discovered FAQs)

## Configuration
- `RAG_ARCHITECTURE_VERSION=v1`
- `RAG_CHUNK_STRATEGY=split`
- `RAG_CONTEXTUAL_ENABLED=false`
- `RAG_RERANK_ENABLED=false`
- `RAG_HYBRID_ENABLED=true`
- `RAG_TOP_K=10`
- Embedding model: `qwen/qwen3-embedding-8b` (4096 dimensions)
- Chat model: `mistralai/devstral-2512:free`

## Results Summary

| Metric | Value |
|--------|-------|
| Total Score | 52/60 (86.7%) |
| Average Score | 2.60/3.00 |
| Average Coverage | 75.0% |
| Average Response Time | 11.8s |

## Rating Distribution

| Rating | Count | Percentage |
|--------|-------|------------|
| Complete (3) | 13 | 65.0% |
| Partial (2) | 6 | 30.0% |
| Minimal (1) | 1 | 5.0% |
| Wrong (0) | 0 | 0.0% |

## Chunks Created
- 128 documents → 387 chunks (split strategy)
