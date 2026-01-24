# Retrieval Enhancement Evaluation Report

**Date:** 2025-01-24
**Branch:** `feature/retrieval-enhancement`
**Model:** `mistralai/mistral-nemo`
**Judge:** `google/gemini-3-flash-preview`
**Dataset:** 27 questions (14 direct, 5 multi-doc, 8 out-of-scope)

## Objective

Evaluate BM25 hybrid search and HyDE query expansion to improve RAG retrieval quality, particularly for multi-doc questions which had low correctness (0.20) in previous evaluations.

## Configurations Tested

| Config | Collection | Retrieval Mode | HyDE | BM25 Normalization |
|--------|------------|----------------|------|-------------------|
| **Baseline** | `infomaniak_full_doc_no_images` | Dense only | No | No |
| **HyDE + Dense** | `infomaniak_hybrid_full_doc_no_images` | Dense only | Yes | No |
| **Normalized BM25 Hybrid** | `infomaniak_hybrid_full_doc_no_images` | Hybrid (RRF) | No | Yes |

### Implementation Details

- **BM25 Normalization:** Transforms kSuite compound terms for better tokenization
  - `"kDrive"` → `"k Drive"`, `"kMeet"` → `"k Meet"`, etc.
- **HyDE:** Generates hypothetical answer document using LLM before embedding
- **Hybrid RRF:** Reciprocal Rank Fusion with k=60, combining dense and sparse results

## Results

### Overall Metrics

| Config | Correctness | Faithfulness | Relevance | Retrieval Latency | Total Latency |
|--------|-------------|--------------|-----------|-------------------|---------------|
| Baseline | 0.696 | 0.807 | 0.774 | 731ms | 2904ms |
| HyDE + Dense | 0.741 | 0.822 | 0.819 | 3423ms | 6423ms |
| **Normalized Hybrid** | **0.765** | 0.819 | 0.800 | **674ms** | **2841ms** |

### Per-Category Breakdown

#### Direct Questions (n=14)
Single-document factual questions.

| Config | Correctness | Relevance |
|--------|-------------|-----------|
| Baseline | 0.771 | 0.907 |
| HyDE + Dense | 0.771 | **0.993** |
| **Normalized Hybrid** | **0.857** | **0.993** |

**Winner:** Normalized Hybrid (+11.2% correctness, +9.5% relevance vs baseline)

#### Multi-Doc Questions (n=5)
Questions requiring information from multiple documents.

| Config | Correctness | Relevance |
|--------|-------------|-----------|
| Baseline | 0.760 | 0.880 |
| **HyDE + Dense** | **0.900** | **0.920** |
| Normalized Hybrid | 0.650 | 0.820 |

**Winner:** HyDE + Dense (+18.4% correctness vs baseline)

#### Out-of-Scope Questions (n=8)
Questions the system should decline to answer.

| Config | Correctness | Relevance |
|--------|-------------|-----------|
| Baseline | 0.525 | 0.475 |
| HyDE + Dense | 0.588 | 0.450 |
| **Normalized Hybrid** | **0.675** | 0.450 |

**Winner:** Normalized Hybrid (+28.6% correctness vs baseline)

### Cost Analysis

| Config | Total Input Tokens | Total Output Tokens | Total Cost | Avg Cost/Query |
|--------|-------------------|---------------------|------------|----------------|
| Baseline | 114,485 | 2,202 | $0.00238 | $0.000088 |
| HyDE + Dense | 107,514 | 2,295 | $0.00224 | $0.000083 |
| Normalized Hybrid | 111,622 | 1,858 | $0.00231 | $0.000085 |

All configurations have similar costs (~$0.0024 for 27 questions).

## Analysis

### Key Findings

1. **Normalized BM25 Hybrid is the best overall choice:**
   - Highest overall correctness (0.765, +9.9% vs baseline)
   - Best for direct questions (+11.2% correctness)
   - Best for out-of-scope handling (+28.6% correctness)
   - Fastest retrieval (674ms, -7.8% vs baseline)
   - No additional latency cost

2. **HyDE excels at multi-doc questions:**
   - Best multi-doc correctness (0.900 vs 0.650 for hybrid)
   - Near-perfect relevance for direct questions (0.993)
   - But adds 2.7s latency per query (3.7x slower retrieval)

3. **Trade-off: Speed vs Multi-Doc Performance:**
   - Hybrid: Fast, great for direct/out-of-scope, weaker on multi-doc
   - HyDE: Slow, best for multi-doc, moderate improvement elsewhere

### Why Hybrid Struggles with Multi-Doc

The RRF fusion may be diluting results when multiple documents are needed:
- Dense search finds semantically similar documents
- BM25 finds keyword-matching documents
- Fusion may surface different documents than pure dense, missing complementary information

### Why HyDE Helps Multi-Doc

HyDE generates a hypothetical answer containing synthesized vocabulary from multiple concepts, which may help the dense embedding capture cross-document relationships.

## Recommendations

### For Production Use

**Recommended: Normalized BM25 Hybrid**
- Best overall quality metrics
- No latency penalty
- Good balance across question types

### For Multi-Doc Heavy Use Cases

Consider a **hybrid approach**:
1. Detect multi-doc questions (e.g., questions with "and", "compare", "both")
2. Use HyDE for detected multi-doc questions
3. Use Normalized Hybrid for all other questions

### Future Improvements

1. **Query Classification:** Train a lightweight classifier to route queries
2. **Tunable RRF:** Experiment with different k values (currently k=60)
3. **Reranking:** Add cross-encoder reranking after hybrid retrieval
4. **Multi-Doc Dataset:** Expand evaluation set with more multi-doc questions

## Conclusion

The Normalized BM25 Hybrid retrieval provides the best overall improvement (+9.9% correctness) with no latency cost. It should be adopted as the default retrieval strategy.

For applications with many multi-document questions, HyDE remains valuable but should be used selectively due to its latency impact.

## Appendix: Evaluation Files

- Baseline: `eval_infomaniak_full_doc_no_images_mistral-nemo_20260124_165942.json`
- HyDE + Dense: `eval_infomaniak_hybrid_full_doc_no_images_mistral-nemo_20260124_170134.json`
- Normalized Hybrid: `eval_infomaniak_hybrid_full_doc_no_images_mistral-nemo_20260124_165942.json`

All results logged to Langfuse with tags: `config:baseline_full`, `config:hyde_dense_full`, `config:normalized_bm25_full`
