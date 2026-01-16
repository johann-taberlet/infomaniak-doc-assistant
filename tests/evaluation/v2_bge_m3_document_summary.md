# V2 Architecture Evaluation Results

**Date:** 2026-01-16
**Documents:** 128 (including 127 auto-discovered FAQs)

## Configuration
- `RAG_ARCHITECTURE_VERSION=v2`
- `RAG_CHUNK_STRATEGY=document` (whole FAQ as single chunk)
- `RAG_CONTEXTUAL_ENABLED=true`
- `RAG_RERANK_ENABLED=false`
- `RAG_HYBRID_ENABLED=true`
- `RAG_TOP_K=10`
- Embedding model: `baai/bge-m3` (1024 dimensions)
- Chat model: `mistralai/devstral-2512:free`

## Results Summary

| Metric | Value |
|--------|-------|
| Total Score | 49/60 (81.7%) |
| Average Score | 2.45/3.00 |
| Average Coverage | 74.5% |
| Average Response Time | 13.1s |

## Rating Distribution

| Rating | Count | Percentage |
|--------|-------|------------|
| Complete (3) | 11 | 55.0% |
| Partial (2) | 7 | 35.0% |
| Minimal (1) | 2 | 10.0% |
| Wrong (0) | 0 | 0.0% |

## Notable Results
- **Zero "Wrong" answers** - All questions got at least minimal relevant response
- **Euria question (Q20):** Partial (66.7%) - Previously failed completely
- **Drop Box question (Q10):** Complete (83.3%) - Previously failed completely
- **Linux install (Q8):** Partial (66.7%) - Previously failed completely

## Weak Points
- Q5 (Record kMeet): Minimal (42.9%)
- Q15 (Create kChat channel): Minimal (40.0%)
