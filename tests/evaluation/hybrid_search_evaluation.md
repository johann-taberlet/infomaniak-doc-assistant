# RAG Evaluation Report: Hybrid Search (BM25 + Vector)

**Date:** 2026-01-16
**Configuration:** RAG_CHUNK_SIZE=1500, RAG_TOP_K=10, RAG_HYBRID_ENABLED=true, RAG_BM25_K=60
**LLM:** mistralai/ministral-8b-2512 (OpenRouter)
**Embeddings:** qwen/qwen3-embedding-8b (OpenRouter)

---

## Summary

| Rating | Count | Percentage |
|--------|-------|------------|
| **Correct** | 10 | 50% |
| **Partial** | 8 | 40% |
| **Wrong** | 2 | 10% |

**Overall Success Rate: 90%** (Correct + Partial)

---

## Detailed Results

| # | Question | Rating | Analysis |
|---|----------|--------|----------|
| 1 | Create kMeet meeting | Partial | Missing webcam/mic access step, "Join the meeting" button |
| 2 | Share screen in kMeet | **Correct** | All key points including iOS limitation |
| 3 | Fix audio in kMeet | Partial | Missing mobile Privacy settings, Firefox WebRTC |
| 4 | Create breakout rooms | **Correct** | Perfect - all moderator controls covered |
| 5 | Record kMeet meeting | **Correct** | Complete with kDrive, .mp4, 3hr limit |
| 6 | Set kMeet password | **Correct** | Security options, protect toggle covered |
| 7 | Livestream kMeet | **WRONG** | RETRIEVAL FAILURE: Document rank 19 (not in top 10) |
| 8 | Install kDrive Linux | **Correct** | AppImage, libfuse2, permissions - all correct |
| 9 | Share file from kDrive | Partial | Missing specific rights levels (view/modify/manage) |
| 10 | Drop Box in kDrive | Partial | Core concept correct, missing advanced options |
| 11 | Resolve sync conflicts | Partial | Missing Rescue Folder, merge options |
| 12 | Manage user rights | Partial | Doesn't clearly explain Admin vs User levels |
| 13 | Access files locally | **Correct** | Lite Sync explained perfectly |
| 14 | Sync with Synology NAS | **Correct** | WebDAV, Cloud Sync, all sync types |
| 15 | Create kChat channel | Partial | Missing General default, convert/archive |
| 16 | Slash commands | **Correct** | Built-in and custom commands covered |
| 17 | Connect external apps | **WRONG** | LLM FAILURE: Doc at rank 2 but not used! |
| 18 | Translate message | **Correct** | Action menu, translate steps correct |
| 19 | Invite external users | Partial | Missing admin requirement, guest permissions |
| 20 | What is Euria | **Correct** | **FIXED!** AI assistant correctly explained |

---

## Key Improvements from Hybrid Search

### Fixed Issues

1. **Euria (Q20):** Previously returned 0% accuracy - semantic search couldn't match "Euria" term.
   Now correctly identifies Euria as AI assistant with usage instructions.

2. **Drop Box (Q10):** Previously failed completely.
   Now partially correct with core concept and basic creation steps.

### BM25 Impact
- Proper nouns (Euria, Drop Box) now retrievable via exact keyword matching
- RRF fusion balances semantic similarity with term frequency

---

## Remaining Issues

### Q7: Livestream - Retrieval Failure
- **Problem:** "Broadcast a kMeet meeting via Live Streaming mode" at rank 19
- **Cause:** Query "livestream" doesn't match doc term "Live Streaming"
- **Fix options:** Increase top_k, query expansion, or re-index with synonyms

### Q17: Webhooks - LLM Generation Failure
- **Problem:** Document "Connect external applications to kChat" retrieved at rank 2
- **Content includes:** webhooks, incoming/outgoing, Integrations menu
- **LLM said:** "documentation does not explicitly explain..."
- **Cause:** Model (ministral-8b) may have context confusion or prompt issues
- **Fix options:** Better model, improved prompt, or context compression

---

## Comparison with Previous Evaluation

| Metric | Before (Pure Vector) | After (Hybrid) | Change |
|--------|---------------------|----------------|--------|
| Correct | ~30% | 50% | +20% |
| Partial | ~22% | 40% | +18% |
| Wrong | ~48% | 10% | -38% |
| **Success** | ~52% | 90% | **+38%** |

---

## Recommendations

1. **Increase RAG_TOP_K to 15** for better coverage
2. **Consider query expansion** for term variations (livestream/streaming)
3. **Evaluate different LLM models** - ministral-8b may be too small
4. **Add synonyms during indexing** for common term variations
