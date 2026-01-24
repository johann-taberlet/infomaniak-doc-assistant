# Evaluation 004: Retrieval Enhancement Research

**Date**: 2026-01-24
**Author**: Engineering Team
**Status**: Research Complete - Ready for Implementation

## Executive Summary

This document presents research findings on **BM25 hybrid search** and **query expansion techniques** to improve retrieval quality in our kSuite RAG system. Based on industry best practices and academic research, we recommend a phased evaluation comparing:

1. **Baseline**: Dense-only retrieval (current system)
2. **BM25 Hybrid**: Dense + Sparse vectors with RRF fusion
3. **Query Expansion**: HyDE and LLM-based query rewriting
4. **Combined**: Hybrid + Query Expansion

## Current Baseline

### System Configuration
From previous evaluations ([002](./002-chunking-strategy-evaluation.md), [003](./003-llm-model-evaluation.md)):

| Component | Selection | Rationale |
|-----------|-----------|-----------|
| **Collection** | `infomaniak_full_doc_no_images` | 0.785 relevance, best chunking |
| **Vectors** | 127 documents, 4096 dimensions | Qwen3-Embedding-4B |
| **LLM** | Mistral Nemo + Large (routed) | Best quality/cost balance |
| **Retrieval** | Dense-only, top-k=5 | Vector similarity search |

### Baseline Performance (27 questions)

| Category | Count | Correctness | Relevance |
|----------|-------|-------------|-----------|
| Direct | 14 | 0.90 | 0.93 |
| Multi-doc | 5 | 0.20 | 0.88 |
| Out-of-scope | 8 | 0.00 | 0.48 |
| **Overall** | **27** | **0.504** | **0.785** |

**Key weakness**: Multi-document questions (0.20 correctness) and vocabulary mismatch.

---

## Dataset Analysis: `cleaned_no_images`

### Corpus Statistics

| Metric | Value |
|--------|-------|
| **Total Documents** | 127 |
| **kDrive** | 83 (65%) |
| **kMeet** | 19 (15%) |
| **kChat** | 25 (20%) |
| **Avg Lines/Doc** | 50.5 |
| **Language** | English |

### Critical Vocabulary Finding

**Documents use "k Drive" (with space), but users type "kDrive" or "kdrive":**

```
Document text: "k Drive", "k Meet", "k Chat", "k Suite"
User queries:  "kDrive",  "kMeet",  "kChat",  "kSuite"
URLs in docs:  "kdrive",  "kmeet",  "kchat"
```

| Pattern | Occurrences | Files |
|---------|-------------|-------|
| `k Drive\|k Meet\|k Chat` (spaced) | 1,169 | 126/127 |
| `kDrive\|kMeet\|kChat` (compact) | 360 | Only in `.images.json` |

**Implication**: BM25 exact matching will **NOT match** user queries like "kDrive sync issue" against documents containing "k Drive synchronization". Dense embeddings handle this naturally.

### Document Structure

All documents follow a consistent markdown structure:

```markdown
# Title with k Product action

Source: https://www.infomaniak.com/en/support/faq/{ID}/{slug}

---

Introduction paragraph explaining the guide.

### Preamble (optional)
- Prerequisites as bullet points
- Cross-references to related FAQs

## Section Heading
1. Numbered procedural steps
2. **Bold** for UI elements
3. `code` for commands
```

### Where BM25 Would Help

| Use Case | Example | BM25 Benefit |
|----------|---------|--------------|
| **System commands** | `SFC /scannow`, `DISM /Online` | Exact match critical |
| **URLs** | `kmeet.infomaniak.com` | Exact phrase |
| **Error messages** | "unrecognized device error" | Verbatim matching |
| **Code blocks** | `explorer.exe`, `.mp4` | Technical terms |

### Where BM25 Would NOT Help

| Use Case | User Query | Document Text | Issue |
|----------|-----------|---------------|-------|
| **Product names** | "kDrive" | "k Drive" | Space mismatch |
| **Feature names** | "video call" | "k Meet meeting" | Vocabulary gap |
| **Concepts** | "security" | "encryption", "password", "protect" | Semantic not lexical |
| **Actions** | "sync files" | "synchronization", "Desktop app" | Word form variance |

### Multi-Document Challenge

**Question**: "What security features are available across kSuite products?"

Requires synthesizing 3 separate documents:

| Document | Key Content |
|----------|-------------|
| `kmeet_2464_secure-a-kmeet-meeting...` | Password, end-to-end encryption, Chromium requirement |
| `kchat_2733_understanding-kchat-data-security.md` | ISO 27001/9001, encrypted at rest/transit, Swiss hosting |
| `kdrive_2462_understanding-kdrive-data-security.md` | AES-128-CBC, SSL/TLS, Tier III+ data centers |

**Vocabulary diversity across security docs**:
- kMeet: "Secure a meeting", "password", "encryption key"
- kChat: "Data Security", "protection of your communications"
- kDrive: "data security and confidentiality", "protection"

None use the phrase "security features" - this is where **HyDE shines** by generating a hypothetical document mentioning all three products.

### Revised Strategy Based on Dataset

| Technique | Expected Impact | Rationale |
|-----------|-----------------|-----------|
| **BM25 Hybrid** | **Low-Medium** (+2-5%) | Product name mismatch limits utility; helps only for exact commands/URLs |
| **Query Expansion** | **High** (+10-20%) | Bridges "kDrive"→"k Drive", "video call"→"k Meet meeting" |
| **HyDE** | **Very High for Multi-doc** | Generates cross-product hypothetical answers |
| **Product Name Normalization** | **High** | Pre-process queries: "kDrive"→"k Drive" before BM25 |

### Recommended Query Preprocessing

```python
def normalize_product_names(query: str) -> str:
    """Normalize compact product names to spaced format for BM25."""
    replacements = {
        "kdrive": "k Drive",
        "kDrive": "k Drive",
        "kmeet": "k Meet",
        "kMeet": "k Meet",
        "kchat": "k Chat",
        "kChat": "k Chat",
        "ksuite": "k Suite",
        "kSuite": "k Suite",
    }
    result = query
    for compact, spaced in replacements.items():
        # Case-insensitive replacement, preserve original for dense
        result = re.sub(rf'\b{compact}\b', spaced, result, flags=re.IGNORECASE)
    return result
```

### Updated Evaluation Priority

Based on dataset analysis:

1. **Priority 1: HyDE Query Expansion** - Highest expected impact for multi-doc and vocabulary gap
2. **Priority 2: Product Name Normalization** - Low-cost preprocessing for BM25 effectiveness
3. **Priority 3: BM25 Hybrid** - Worth testing but tempered expectations
4. **Priority 4: Multi-Query (3 products)** - For cross-product questions, explicitly query each product

---

## Research Findings

### 1. BM25 Hybrid Search

#### Why Hybrid Outperforms Single-Method Retrieval

| Method | Strengths | Weaknesses |
|--------|-----------|------------|
| **Dense (Semantic)** | Paraphrases, synonyms, conceptual matching | Misses exact terms, error codes, product names |
| **Sparse (BM25)** | Exact matching, technical terms, SKUs | No semantic understanding, vocabulary mismatch |
| **Hybrid (RRF)** | Best of both worlds | Slightly higher latency |

**Industry benchmarks** ([MongoDB](https://www.mongodb.com/resources/basics/reciprocal-rank-fusion), [ML6](https://www.ml6.eu/en/blog/elevating-your-retrieval-game-insights-from-real-world-deployments)):
- Hybrid (RRF): **NDCG@10 = 0.85** vs Dense-only: 0.72 (+18%)
- With reranking: **NDCG@10 = 0.93** (+28% over baseline)
- Hallucination reduction: **35%** with reranked results

#### Reciprocal Rank Fusion (RRF)

RRF is the recommended fusion method for combining dense and sparse results:

```python
# RRF Score Formula
rrf_score = sum(1 / (k + rank_i) for each retriever)
# k = 60 (standard constant, well-tested across datasets)
```

**Why RRF over score-based fusion**:
- Score distributions differ (cosine: [-1,1] vs BM25: unbounded)
- RRF uses rank positions only, avoiding normalization issues
- Robust in zero-shot scenarios without labeled data

#### Qdrant Native Implementation

Qdrant supports BM25 natively via sparse vectors ([Qdrant docs](https://qdrant.tech/articles/sparse-vectors/)):

```python
from qdrant_client.models import SparseVector, Modifier

# Collection with both dense and sparse vectors
client.create_collection(
    collection_name="hybrid_collection",
    vectors_config={"dense": VectorParams(size=4096, distance=Distance.COSINE)},
    sparse_vectors_config={
        "sparse": SparseVectorParams(modifier=Modifier.IDF)  # BM25-style
    }
)
```

**Implementation options**:
1. **FastEmbed BM25**: `SparseTextEmbedding(model_name="Qdrant/bm25")` - simplest
2. **rank-bm25 library**: Manual TF-IDF sparse vector generation
3. **Qdrant BM42**: Newer hybrid approach, but BM25 is more proven

### 2. Query Expansion Techniques

#### 2.1 HyDE (Hypothetical Document Embeddings)

**How it works** ([ACL 2023 paper](https://aclanthology.org/2023.acl-long.99/)):
1. LLM generates a **hypothetical answer** to the query (may contain hallucinations)
2. Embed the hypothetical document instead of the query
3. Retrieve similar real documents
4. Generate final answer from real documents

**Research results**:
- Outperforms BM25 in 3/4 multilingual datasets
- Outperforms fine-tuned ContrieverFT in 4/8 datasets
- Most effective for abstract/vague queries

**Trade-offs**:
| Pros | Cons |
|------|------|
| No training required (zero-shot) | +1 LLM call per query (latency) |
| Bridges vocabulary gap | Quality depends on LLM capability |
| Works across languages | May not help already specific queries |

**When HyDE helps most**:
- Vague questions: "How do I use the security features?"
- Vocabulary mismatch: User says "video call" but docs say "kMeet conference"
- Multi-doc synthesis: Hypothetical answer can mention multiple products

#### 2.2 LLM Query Rewriting

Simpler than HyDE - rephrase the query for better retrieval:

```python
rewrite_prompt = """
Rewrite this user question to improve retrieval from kSuite documentation.
- Add product names (kDrive, kMeet, kChat) if implied
- Expand abbreviations
- Add synonyms for technical terms

Original: {query}
Rewritten:
"""
```

**Techniques**:
1. **Synonym expansion**: "video call" → "video call kMeet conference"
2. **Multi-query generation**: Generate 3 variants, retrieve from all, deduplicate
3. **Step-back prompting**: Generate broader query first, then specific

#### 2.3 HyPE (Hypothetical Prompt Embeddings)

A newer alternative ([2024 research](https://aisel.aisnet.org/wi2024/115/)):
- Pre-generates hypothetical documents at **indexing time** (not query time)
- No LLM call during retrieval
- Up to **45% improvement** in claim recall

**Trade-off**: Increased storage but faster inference.

### 3. Reranking (Future Enhancement)

Cross-encoder reranking after retrieval provides additional gains:
- **+28% NDCG@10** improvement over baseline
- **35% reduction** in LLM hallucinations
- Options: `ms-marco-MiniLM-L-6-v2`, `bge-reranker-base`

**Recommendation**: Evaluate reranking after BM25/query expansion baseline is established.

---

## Evaluation Plan

### Phase 1: Mini-Eval (10 questions)

Quick iteration to validate implementations before full evaluation.

| # | Configuration | Description | Expected Latency | Priority |
|---|---------------|-------------|------------------|----------|
| 1 | `baseline` | Current dense-only | ~1.4s | Reference |
| 2 | `hyde_dense` | HyDE + Dense (no hybrid) | ~3s | **HIGH** |
| 3 | `normalized_bm25` | Query normalization + BM25 Hybrid | ~1.6s | Medium |
| 4 | `bm25_hybrid` | Dense + Sparse RRF (no normalization) | ~1.6s | Low |
| 5 | `hyde_hybrid` | HyDE + Normalized Hybrid | ~3.5s | **HIGH** |

**Rationale for priority order**:
1. HyDE addresses the main weakness (vocabulary gap, multi-doc)
2. Normalization makes BM25 viable despite "k Drive" vs "kDrive" mismatch
3. Raw BM25 hybrid likely to underperform without normalization

**Mini-eval questions** (from evaluation dataset):
- 5 direct (including product-specific terms like "kDrive", "kMeet")
- 3 multi-doc (security across products, kChat+kMeet integration)
- 2 out-of-scope

### Phase 2: Full Evaluation (27 questions)

Complete evaluation on winning configurations from Phase 1.

### Metrics

| Metric | Weight | Target | Description |
|--------|--------|--------|-------------|
| **Relevance** | 30% | >0.85 | Retrieved context quality |
| **Correctness** | 40% | >0.60 | Answer accuracy vs expected |
| **Faithfulness** | 20% | >0.80 | Grounding in context |
| **Latency** | 10% | <3s | End-to-end response time |

**Composite Score**:
```python
score = 0.4*correctness + 0.3*relevance + 0.2*faithfulness + 0.1*(1 - latency/5)
```

### Category-Specific Expectations

| Category | Current | BM25 Hybrid | HyDE | Combined |
|----------|---------|-------------|------|----------|
| Direct | 0.93 | 0.95 (+2%) | 0.93 | 0.95 |
| Multi-doc | 0.88 | 0.92 (+5%) | 0.95 (+8%) | 0.96 |
| OOS | 0.48 | 0.50 | 0.55 | 0.55 |

**Rationale**:
- BM25 helps direct questions with exact term matching
- HyDE helps multi-doc by generating synthetic cross-product answers
- OOS improvement limited (correct behavior is to abstain)

---

## Implementation Approach

### 1. BM25 Hybrid (Recommended First)

```python
# backend/app/rag/hybrid_retriever.py

from fastembed import SparseTextEmbedding

class HybridRetriever:
    def __init__(self, collection_name: str):
        self.dense_embedder = get_embeddings()
        self.sparse_embedder = SparseTextEmbedding("Qdrant/bm25")

    def search(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        # Prefetch from both indexes
        results = self.client.query_points(
            collection_name=self.collection_name,
            prefetch=[
                Prefetch(query=dense_embedding, using="dense", limit=20),
                Prefetch(query=sparse_embedding, using="sparse", limit=20),
            ],
            query=FusionQuery(fusion=Fusion.RRF),  # RRF fusion
            limit=top_k,
        )
        return results
```

**Required changes**:
1. Create new collection with sparse vectors
2. Re-ingest documents with BM25 sparse embeddings
3. Modify retriever to use Query API with prefetch
4. Run evaluation with Langfuse tags

### 2. Query Expansion (HyDE) - Dataset-Optimized

```python
# backend/app/rag/query_expansion.py

class HyDEExpander:
    def __init__(self, model: str = "mistralai/mistral-nemo"):
        self.llm = get_llm(model)

    def expand(self, query: str) -> str:
        # Dataset-specific prompt using actual document vocabulary
        prompt = f"""You are Infomaniak k Suite documentation. Write a FAQ answer to this question.

IMPORTANT: Use these exact product names with space:
- "k Drive" (not kDrive) for cloud storage
- "k Meet" (not kMeet) for video conferencing
- "k Chat" (not kChat) for messaging
- "k Suite" (not kSuite) for the product suite

Use vocabulary from the documentation:
- "synchronization" not "sync"
- "video conference" or "meeting" not "video call"
- "encryption key" and "password protection" for security
- "Infomaniak Manager" for admin dashboard

Question: {query}

Answer (1 paragraph, mention specific products and features):"""
        return self.llm.generate(prompt)
```

**Why this matters for our dataset**:
- Documents use "k Drive" (spaced) - HyDE output must match
- Technical terms like "synchronization" appear more than "sync"
- Cross-product mentions help retrieve multi-doc answers

**Cache strategy**:
- During evaluation, cache HyDE expansions to avoid redundant LLM calls
- In production, consider HyPE (pre-indexed hypothetical docs)

### 3. Combined Approach

```python
def hybrid_hyde_search(query: str) -> list[RetrievalResult]:
    # 1. Generate hypothetical document
    hyde_doc = hyde_expander.expand(query)

    # 2. Embed both original and HyDE
    query_dense = embedder.embed(query)
    hyde_dense = embedder.embed(hyde_doc)

    # 3. BM25 on original query only (exact matching)
    query_sparse = sparse_embedder.embed(query)

    # 4. Multi-query hybrid fusion
    results = client.query_points(
        prefetch=[
            Prefetch(query=query_dense, using="dense", limit=15),
            Prefetch(query=hyde_dense, using="dense", limit=15),
            Prefetch(query=query_sparse, using="sparse", limit=15),
        ],
        query=FusionQuery(fusion=Fusion.RRF),
        limit=5,
    )
    return results
```

---

## Expected Outcomes (Dataset-Adjusted)

### Per-Configuration Predictions

| Configuration | Relevance | Correctness | Multi-doc | Notes |
|---------------|-----------|-------------|-----------|-------|
| `baseline` | 0.785 | 0.504 | 0.20 | Current |
| `bm25_hybrid` (raw) | 0.79 | 0.51 | 0.22 | Limited by "k Drive"≠"kDrive" |
| `normalized_bm25` | 0.82 | 0.55 | 0.30 | Normalization unlocks BM25 |
| `hyde_dense` | **0.85** | **0.60** | **0.50** | Vocabulary bridging works |
| `hyde_hybrid` | **0.87** | **0.62** | **0.55** | Best expected |

### Why HyDE > BM25 for This Dataset

1. **Product name mismatch**: BM25 can't match "kDrive" → "k Drive" without preprocessing
2. **Vocabulary diversity**: "video call" vs "k Meet meeting" requires semantic understanding
3. **Multi-doc synthesis**: HyDE generates text mentioning all products, improving recall

### Realistic Improvement Targets

| Metric | Baseline | Target | Expected Config |
|--------|----------|--------|-----------------|
| Relevance | 0.785 | >0.85 | HyDE + Hybrid |
| Overall Correctness | 0.504 | >0.58 | HyDE + Hybrid |
| **Multi-doc Correctness** | **0.20** | **>0.45** | **HyDE** (primary driver) |
| Direct Correctness | 0.90 | >0.92 | Normalized BM25 |

### Cost Impact

| Configuration | LLM Calls/Query | Est. Cost (1K queries) | ROI |
|---------------|-----------------|------------------------|-----|
| Baseline | 1 (generation) | $0.08 | - |
| Normalized BM25 | 1 | $0.08 | Free if it works |
| HyDE | 2 (+expansion) | $0.16 | 2x cost, but +125% multi-doc |
| HyDE + Hybrid | 2 | $0.16 | Best quality/cost |

**Key Insight**: Given the dataset characteristics, HyDE is likely more impactful than BM25. BM25 requires query normalization to be effective at all.

---

## Decision Framework

After evaluation, select configuration based on:

```python
def select_configuration(results: dict) -> str:
    """Select best configuration based on evaluation results."""

    # Primary metric: Multi-doc improvement (biggest weakness)
    if results["hyde_hybrid"]["multi_doc"] > 0.45:
        if results["hyde_hybrid"]["latency"] < 4.0:
            return "hyde_hybrid"  # Best quality
        else:
            return "hyde_dense"  # HyDE without hybrid for speed

    # If HyDE underperforms, check if BM25 helps
    if results["normalized_bm25"]["relevance"] > 0.82:
        return "normalized_bm25"  # Cheap improvement

    # Fallback: Keep baseline if nothing helps
    return "baseline"
```

**Decision thresholds**:
- Multi-doc correctness must reach >0.45 (from 0.20) to justify HyDE cost
- Latency must stay <4s for acceptable UX
- BM25 only worthwhile with normalization preprocessing

---

## Next Steps (Revised Priority)

1. **Implement HyDE query expander** with dataset-specific prompt
   - Use vocabulary from actual documents ("k Drive", "synchronization")
   - Cache expansions during evaluation

2. **Implement query normalization** for BM25
   - "kDrive" → "k Drive" preprocessing
   - Apply to sparse vector queries only

3. **Create hybrid collection** with dense + sparse vectors
   - Re-ingest 127 documents with BM25 sparse embeddings
   - Use Qdrant FastEmbed integration

4. **Run mini-eval** (10 questions) comparing:
   - baseline vs hyde_dense vs normalized_bm25 vs hyde_hybrid

5. **Run full evaluation** (27 questions) on top 2 configurations

6. **Document results** in 005-retrieval-enhancement-evaluation.md

7. **Production decision**: Select final configuration

---

## References

### Hybrid Search
- [Qdrant Sparse Vectors](https://qdrant.tech/articles/sparse-vectors/)
- [Qdrant Hybrid Search Revamped](https://qdrant.tech/articles/hybrid-search/)
- [MongoDB RRF Explained](https://www.mongodb.com/resources/basics/reciprocal-rank-fusion)
- [Dense vs Sparse vs Hybrid RRF](https://medium.com/@robertdennyson/dense-vs-sparse-vs-hybrid-rrf-which-rag-technique-actually-works-1228c0ae3f69)

### Query Expansion
- [HyDE Paper (ACL 2023)](https://aclanthology.org/2023.acl-long.99/)
- [Query Rewriting Guide](https://medium.com/@florian_algo/advanced-rag-06-exploring-query-rewriting-23997297f2d1)
- [LlamaIndex Query Transform Cookbook](https://docs.llamaindex.ai/en/stable/examples/query_transformations/query_transform_cookbook/)

### Evaluation
- [RAG Evaluation Metrics](https://www.geeksforgeeks.org/nlp/evaluation-metrics-for-retrieval-augmented-generation-rag-systems/)
- [ML6 Production RAG Insights](https://www.ml6.eu/en/blog/elevating-your-retrieval-game-insights-from-real-world-deployments)
- [Reranking Guide 2025](https://www.zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025)

---

## Artifacts

| File | Purpose |
|------|---------|
| `backend/app/rag/hybrid_retriever.py` | Hybrid search implementation (to create) |
| `backend/app/rag/query_expansion.py` | HyDE/rewriting implementation (to create) |
| `scripts/ingest_hybrid.py` | Re-ingestion with sparse vectors (to create) |
| `data/evaluations/004_*.json` | Evaluation results (to generate) |
