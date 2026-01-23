# ADR-002: Data Cleaning Strategy

**Status**: Accepted
**Date**: 2025-01-23
**Context**: RAG pipeline data preparation

## Problem

Raw scraped documentation contains artifacts that can pollute RAG retrieval and generation:

1. **Invisible characters** - Zero-width joiners, BOM markers affect tokenization
2. **Scraping artifacts** - Stuck words (`Downloadthe`), orphan punctuation
3. **Images** - Screenshots may be retrieved out of context, leading to irrelevant visuals in responses

## Decision

We produce **two cleaned datasets** from raw data to enable A/B testing:

| Dataset | Path | Image Handling | Use Case |
|---------|------|----------------|----------|
| **Inline** | `data/cleaned/` | Images stay in markdown | Simple RAG, images in chunks |
| **Structured** | `data/cleaned_no_images/` | Images extracted to JSON | Controlled image injection |

## Data Flow

```
data/raw/           (source of truth - never modified)
    ↓
scripts/clean_docs.py
    ↓
├── data/cleaned/              (images inline)
└── data/cleaned_no_images/    (images as metadata)
    ├── *.md                   (text only)
    └── *.images.json          (structured image data)
```

## Cleaning Operations

### Text Cleaning (Both Datasets)

| Operation | Before | After | Rationale |
|-----------|--------|-------|-----------|
| Remove zero-width chars | `Download​the` | `Downloadthe` | Affects tokenization |
| Fix stuck words | `Downloadthe` | `Download the` | Improves retrieval |
| Fix missing spaces | `].Click` | `]. Click` | Proper sentence boundaries |
| Remove orphan punctuation | Line with just `:` | (removed) | Leftover from images |
| Collapse blank lines | `\n\n\n\n` | `\n\n` | Reduces noise |
| Trim whitespace | `text   \n` | `text\n` | Cleaner chunks |

### Image Extraction (Structured Dataset Only)

Images are removed from text and stored with context:

```json
{
  "faq_id": "2475",
  "title": "Create a kMeet meeting",
  "source_url": "https://...",
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

**Metadata captured:**
- `heading` - Parent section (## heading)
- `step` - Step number if in ordered list (1, 2, 3...)
- `context` - Surrounding text (truncated to 200 chars)

## Image Strategy Rationale

### Problem with Inline Images

In v1, images were kept inline but chunking broke context:

```
Chunk A: "1. Click Settings ![image](url1)"
Chunk B: "2. Enable sync ![image](url2)"      ← Retrieved
Chunk C: "3. Save changes ![image](url3)"
```

If Chunk B is retrieved for a different question, `url2` might appear in the response even though it's irrelevant.

### Structured Approach Benefits

1. **Controlled injection** - Only add images when response matches heading/step
2. **Evaluation possible** - Can measure image relevance separately
3. **Smaller chunks** - 12% size reduction without images
4. **Fallback** - Can always ignore images if they hurt quality

### When to Inject Images (Generation Time)

```python
# Pseudocode for image injection
if response_contains_steps and chunk_heading in image_metadata:
    matching_images = [
        img for img in images
        if img.heading == chunk_heading
        and img.step in response_steps
    ]
    # Include only highly relevant images
```

## Metrics

| Metric | Raw | Cleaned (inline) | Cleaned (no images) |
|--------|-----|------------------|---------------------|
| Total chars | 420,589 | 422,259 | 370,098 |
| Change | - | +0.4%* | -12.0% |
| Documents | 127 | 127 | 127 |
| Images | 576 | 576 (inline) | 576 (JSON) |

*Slight increase due to adding spaces in stuck words

## Evaluation Plan

Compare both datasets on:

1. **Retrieval quality** - Are correct chunks retrieved?
2. **Answer correctness** - Is the answer accurate?
3. **Image relevance** - When images appear, are they helpful?
4. **Faithfulness** - Is the answer grounded in retrieved context?

## Files

| File | Purpose |
|------|---------|
| `scripts/scrape_docs.py` | Fetch raw docs → `data/raw/` |
| `scripts/clean_docs.py` | Clean → `data/cleaned/` + `data/cleaned_no_images/` |

## Commands

```bash
# Re-scrape all docs (preserves images)
uv run python scripts/scrape_docs.py --force

# Clean and produce both datasets
uv run python scripts/clean_docs.py

# Preview without writing
uv run python scripts/clean_docs.py --dry-run
```

## References

- [PROJECT_ROADMAP.md](../../PROJECT_ROADMAP.md) - Overall project plan
- [ADR-001](./001-frontend-sdk-selection.md) - Frontend SDK decision
