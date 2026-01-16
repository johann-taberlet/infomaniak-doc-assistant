# RAG Research Prompt

Use this prompt with Perplexity, Claude, or any research tool to find optimal RAG strategies.

---

## Context

I'm building a **documentation chatbot** for a SaaS company (cloud storage, video conferencing, team chat). The chatbot answers user questions by retrieving relevant documentation and generating responses.

### Data Characteristics

- **Format:** Markdown files (`.md`)
- **Structure:** FAQ-style articles - each file covers ONE topic/question
- **Total documents:** ~60 articles across 3 products
- **Document lengths:**
  - Minimum: ~900 characters
  - Maximum: ~7,500 characters
  - Average: ~3,000 characters
  - Median: ~2,500 characters
- **Content type:** How-to guides, troubleshooting steps, feature explanations
- **Language:** English (but users may query in French, German, or Italian)

### Document Structure Example

```markdown
# How to [do something]

This guide explains how to [task description].

### Prerequisites
- Requirement 1
- Requirement 2

## Step-by-step instructions

1. First step with details...
2. Second step with details...
3. Third step with details...

## Troubleshooting

- If X happens, do Y
- If Z happens, do W

Source: [link to documentation]
```

### Query Characteristics

- Natural language questions ("How do I record a meeting?")
- Feature lookups ("What is Euria?")
- Troubleshooting ("My audio isn't working")
- May include proper nouns and product-specific terms
- May be in different languages than the documentation

### Current Challenges

1. **Proper noun matching:** Users ask about "Euria" or "Drop Box" but semantic search misses exact term matches
2. **Terminology gaps:** Users say "livestream" but docs say "broadcast" or "live streaming"
3. **Context fragmentation:** When documents are split into chunks, related information gets separated
4. **Multi-document answers:** Some questions require synthesizing info from multiple articles

---

## Research Questions

Given this specific context (small corpus of ~60 FAQ-style documents, 900-7500 chars each, single-topic articles), what are the **best practices and state-of-the-art techniques** for:

### 1. Chunking Strategy
- Should I use the whole document as a single chunk (since each is already a coherent FAQ)?
- Or split into smaller chunks? If so, what size and overlap?
- Are there hybrid approaches (e.g., hierarchical chunking, parent-child chunks)?
- How does document length distribution affect this choice?

### 2. Embedding Models
- Which embedding models work best for FAQ/documentation retrieval?
- Should I use different models for short vs. long texts?
- What embedding dimensions are optimal for ~60 documents?
- Are there multilingual embedding models that handle cross-language queries well?

### 3. Retrieval Strategy
- Dense retrieval (vector search) vs. sparse (BM25) vs. hybrid - which is best for FAQ retrieval?
- What fusion methods work best (RRF, weighted combination, learned fusion)?
- How many documents should be retrieved (top-k) for a small corpus?
- Should I use different strategies for different query types?

### 4. Query Processing
- Query expansion techniques for terminology gaps (synonyms, paraphrasing)
- Query translation for multilingual support
- Query decomposition for complex questions
- HyDE (Hypothetical Document Embeddings) - is it useful for FAQ retrieval?

### 5. Reranking
- Should I add a reranking step after initial retrieval?
- Cross-encoder rerankers vs. other approaches
- Is reranking worth it for a small corpus?
- Which reranking models work best for documentation?

### 6. Context Assembly
- How to format retrieved documents for the LLM?
- Should I include metadata (title, source URL)?
- How to handle multiple retrieved documents?
- Context compression techniques - are they useful here?

### 7. Answer Generation
- Prompt engineering for documentation QA
- How to make the LLM cite sources accurately?
- Handling "I don't know" when info isn't in the docs
- Reducing hallucination in documentation contexts

### 8. Evaluation & Monitoring
- Best metrics for FAQ retrieval quality (MRR, NDCG, recall@k)?
- How to build a good evaluation dataset?
- Monitoring retrieval quality in production
- A/B testing strategies for RAG improvements

### 9. Advanced Techniques
- Knowledge graphs for documentation
- Late interaction models (ColBERT)
- Contextual retrieval (adding context to chunks before embedding)
- Fine-tuning embeddings on domain-specific data
- Agentic RAG approaches

---

## Constraints

- **Budget-conscious:** Prefer techniques that don't require expensive fine-tuning
- **Latency-sensitive:** Real-time chat, responses should be fast
- **Small corpus:** Only ~60 documents, so some techniques may be overkill
- **Maintainability:** Prefer simpler solutions that are easy to update

---

## Desired Output

Please provide:
1. **Recommended architecture** for this specific use case
2. **Specific models/tools** to use at each stage
3. **Configuration parameters** (chunk size, top-k, etc.)
4. **Trade-offs** for each recommendation
5. **Implementation priority** - what will have the biggest impact?
