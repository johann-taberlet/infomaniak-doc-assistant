# Evaluation 001: Data Cleaning Strategy

**Date**: 2025-01-23
**Author**: Engineering Team
**Status**: Completed

## Executive Summary

This evaluation documents the data cleaning strategy for the Infomaniak kSuite documentation RAG pipeline. We produced two cleaned datasets to enable controlled experimentation with image handling strategies.

## Context

### Source Data

The raw documentation was scraped from Infomaniak's FAQ system:
- **127 documents** covering kDrive, kMeet, and kChat
- **576 embedded images** (screenshots, UI guides)
- **420,589 total characters**

### Identified Problems

During initial analysis, we discovered several data quality issues:

| Problem | Example | Impact on RAG |
|---------|---------|---------------|
| Zero-width characters | `Download​the` (invisible joiner) | Corrupts tokenization |
| Stuck words | `Downloadthe`, `Clickhere` | Poor retrieval matching |
| Missing spaces after punctuation | `].Click` | Sentence boundary issues |
| Orphan punctuation | Lines with just `:` or `.` | Noise in chunks |
| Excessive blank lines | 4+ consecutive newlines | Wasted context window |
| Inline images | `![](url)` scattered in text | Out-of-context retrieval |

## Methodology

### Dual Dataset Strategy

We decided to produce **two cleaned datasets** rather than one, enabling A/B testing of image handling:

```
data/raw/                    (source of truth)
    ↓
scripts/clean_docs.py
    ↓
├── data/cleaned/            (images inline in markdown)
└── data/cleaned_no_images/  (images extracted to JSON)
```

### Cleaning Operations Applied

All cleaning operations are deterministic and reproducible:

1. **Remove zero-width characters**: Unicode categories Cf, Cc (except newlines)
2. **Fix stuck words**: Pattern matching for `word][Word` → `word] [Word`
3. **Add missing spaces**: After punctuation before uppercase letters
4. **Remove orphan punctuation**: Lines containing only `:`, `.`, or whitespace
5. **Collapse blank lines**: Maximum 2 consecutive newlines
6. **Trim trailing whitespace**: Per-line cleanup

### Image Extraction (No-Images Dataset)

For the structured dataset, images are extracted with contextual metadata:

```json
{
  "faq_id": "2475",
  "title": "Create a kMeet meeting",
  "images": [
    {
      "url": "https://faq.storage5.infomaniak.com/...",
      "heading": "Create a virtual meeting room",
      "step": 2,
      "context": "2. Start a new meeting:"
    }
  ]
}
```

This enables **controlled image injection** at generation time rather than random retrieval.

## Results

### Dataset Statistics

| Metric | Raw | Cleaned (inline) | Cleaned (no images) |
|--------|-----|------------------|---------------------|
| Total characters | 420,589 | 422,259 (+0.4%) | 370,098 (-12.0%) |
| Documents | 127 | 127 | 127 |
| Images | 576 | 576 (inline) | 576 (in JSON) |
| Avg doc size | 3,311 chars | 3,324 chars | 2,914 chars |

The +0.4% increase in the inline dataset comes from adding spaces in stuck words.

### Quality Improvements

Manual inspection of 20 random documents confirmed:
- Zero stuck words remaining
- Proper sentence boundaries
- Clean paragraph separation
- No orphan punctuation artifacts

## Decision

**Selected approach**: Dual dataset strategy with both variants available for evaluation.

### Rationale

1. **Flexibility**: Can compare image handling strategies empirically
2. **No data loss**: Original images preserved in JSON metadata
3. **Smaller chunks**: 12% reduction enables more context per retrieval
4. **Future-proof**: Structured images enable smart injection later

## Next Steps

1. Evaluate both datasets with different chunking strategies (see [002-chunking-strategy-evaluation.md](./002-chunking-strategy-evaluation.md))
2. Measure retrieval quality difference between inline vs no-images
3. Implement controlled image injection based on evaluation results

## Artifacts

| File | Purpose |
|------|---------|
| `scripts/clean_docs.py` | Cleaning pipeline |
| `data/cleaned/` | Inline images dataset |
| `data/cleaned_no_images/` | Structured images dataset |
| `docs/decisions/002-data-cleaning-strategy.md` | ADR with full details |
