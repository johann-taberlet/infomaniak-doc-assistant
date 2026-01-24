# Methodology Overview

This document summarizes the systematic approach used to build the kSuite Documentation Assistant, an AI-powered RAG system for Infomaniak's kDrive, kMeet, and kChat products.

## Evaluation-Driven Development

Every component was selected through rigorous A/B testing against a curated set of 27 evaluation questions spanning direct lookups, multi-document reasoning, and out-of-scope queries. Each decision is documented with reproducible benchmarks.

## Pipeline Components

### 1. Data Preparation

**Challenge:** Raw scraped documentation contains embedded images, inconsistent formatting, and navigation artifacts.

**Approach:** Created two dataset variants (with/without inline images) and evaluated retrieval quality on both.

**Result:** `cleaned_no_images` - 12% smaller chunks with cleaner text. Images preserved in separate JSON for future smart injection.

### 2. Chunking Strategy

**Challenge:** FAQ-style documentation has inherent structure (question → answer → steps) that must be preserved.

**Approach:** Tested 4 strategies: full document, recursive (1000/1500 chars), semantic. Measured relevance and answer correctness.

**Result:** `full_document` - FAQs are atomic units averaging 2,914 characters. Splitting breaks coherence and reduces relevance by 9%.

### 3. Retrieval Architecture

**Challenge:** Balance semantic understanding (dense vectors) with exact term matching (sparse/BM25) for product names like "kDrive".

**Approach:** Tested dense-only, sparse-only, and hybrid configurations. Also evaluated HyDE query expansion.

**Result:** `Normalized BM25 Hybrid` - +9.9% correctness over baseline with the fastest latency. BM25 normalization handles kSuite-specific vocabulary.

### 4. Generation Model

**Challenge:** Balance quality, cost ($0.00008 vs $0.0088 per query), and latency for production deployment.

**Approach:** Benchmarked 4 models (Mistral Large, Mistral Nemo, Qwen3-8B, GLM-4.7-Flash) on answer correctness.

**Result:** `Mistral Nemo (12B)` as primary - 113x cheaper than flagship with 83% of the quality. Mistral Large reserved for complex queries.

## Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Relevance | Do retrieved docs contain the answer? (LLM judge) | > 0.75 |
| Correctness | Is the generated answer accurate? (LLM judge) | > 0.70 |
| Latency | End-to-end response time | < 5s |
| Cost | Per-query cost via OpenRouter | < $0.001 |

## Final Performance

| Metric | Value |
|--------|-------|
| Correctness | 0.765 |
| Relevance | 0.800 |
| Latency | ~2.8s |
| Cost | ~$0.00009/query |

## Detailed Reports

- [Data Cleaning Evaluation](evaluations/001-data-cleaning-evaluation.md)
- [Chunking Strategy Evaluation](evaluations/002-chunking-strategy-evaluation.md)
- [LLM Model Evaluation](evaluations/003-llm-model-evaluation.md)
- [Retrieval Enhancement Research](evaluations/004-retrieval-enhancement-research.md)
- [Retrieval Enhancement Evaluation](evaluations/005-retrieval-enhancement-evaluation.md)
- [Complete Summary](evaluations/000-evaluation-summary.md)
