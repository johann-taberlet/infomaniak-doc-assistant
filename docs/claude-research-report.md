# Handling Images in RAG Systems: A Complete Technical Guide for Documentation Assistants

For FAQ documentation systems with UI screenshots, the optimal approach in 2025 combines **pre-captioning at ingestion using Gemini 2.5 Flash Batch** (costing under $1 for 800 images) with **selective runtime vision** for visual queries—a hybrid architecture that preserves your existing Qwen3-embedding-8b + Qdrant stack while adding robust image understanding. This approach outperforms pure multimodal embeddings for text-heavy UI content while maintaining sub-2-second latency at inference time.

The core insight from recent production deployments is that UI screenshots benefit more from detailed text descriptions than from visual embeddings like CLIP. Microsoft's ISE team found that **separate image chunks with detailed captions significantly outperform inline approaches** for both retrieval recall and image citation accuracy. For your 300-800 screenshots across 128 documents, this translates to a straightforward enhancement of your existing text-based pipeline rather than a complex multimodal overhaul.

---

## Vision models excel at UI captioning when prompted correctly

The landscape of vision models has matured considerably, with **batch processing APIs reducing costs by 50%** across all major providers. For UI screenshot captioning specifically, Gemini 2.5 Flash Batch offers the best value at $0.15 per million input tokens and $1.25 per million output tokens—processing your entire screenshot corpus for approximately $0.31. Claude 3.5 Sonnet provides superior OCR accuracy for capturing button text and menu labels, though at roughly 6x the cost.

Open-source alternatives have reached production quality. Qwen2.5-VL-7B demonstrates excellent document and UI understanding with native structured output support, making it viable for organizations requiring on-premise processing. InternVL2.5 achieves comparable accuracy to commercial models, while MiniCPM-V 2.6 enables edge deployment scenarios.

The critical factor for UI screenshots is prompt engineering. Generic image captioning prompts miss the actionable details users need. An effective UI captioning prompt should extract the screen title, enumerate all interactive elements with their exact text labels, list available user actions, and capture any visible error messages or notifications. Structured JSON output enables consistent downstream processing:

```json
{
  "screen_title": "Share Settings Dialog",
  "product": "kDrive",
  "screen_type": "dialog",
  "ui_elements": [
    {"type": "button", "label": "Share", "purpose": "opens sharing options"},
    {"type": "dropdown", "label": "Permission level", "options": ["Viewer", "Editor"]}
  ],
  "visible_text": ["Share with others", "Anyone with the link can view"],
  "user_actions": ["Share file via email", "Copy shareable link", "Set access permissions"]
}
```

The prompt should explicitly request all visible text since this powers keyword search, and should capture the semantic purpose of elements (what they do, not just what they say).

---

## Caption-enriched text chunks integrate seamlessly with existing pipelines

Rather than adopting complex multimodal embeddings, the most practical path enriches your existing text chunks with image descriptions. This approach works with your current Qwen3-embedding-8b model and Qdrant hybrid search without architectural changes. Research comparing approaches shows that caption-based retrieval achieves **approximately 70% of the quality of true multimodal embeddings** while requiring zero infrastructure changes.

The recommended storage pattern treats each image caption as a separate chunk, linked to its source document and surrounding context. Your Qdrant collection schema should include:

```python
vectors_config={
    "text": VectorParams(size=4096, distance=Distance.COSINE)  # Qwen3 dimension
},
sparse_vectors_config={
    "sparse": SparseVectorParams()  # For BM25 hybrid search
}
```

Each image point carries metadata associating it with its parent document, page location, and image type (screenshot, diagram, icon). Including **200-300 characters of surrounding text context** in the caption significantly improves retrieval quality by providing semantic anchoring—the text near an image often describes what the image shows.

For scenarios requiring higher visual fidelity, a phased upgrade path exists. Phase 2 adds SigLIP embeddings as a secondary named vector, enabling cross-modal search where text queries can directly match image content. Phase 3 deploys ColQwen2 for document-level visual retrieval, though this increases storage by approximately 1,024x per page due to multi-vector representations.

---

## Hybrid architecture balances quality, cost, and latency

The production-proven architecture combines pre-captioning for retrieval with selective runtime vision for generation. At ingestion time, a vision model processes each screenshot to produce detailed text descriptions, which are then embedded and indexed alongside regular text chunks. At inference time, the system retrieves relevant chunks (both text and image captions) and only fetches raw images when the query specifically requires visual context.

```
INGESTION: Screenshot → Classify (filter logos) → Vision LLM caption → 
           Embed caption → Store in Qdrant with image_url metadata

INFERENCE: Query → Embed → Retrieve top-k chunks → 
           If visual query AND image chunk: fetch raw image →
           Mistral Large generates response
```

The classification layer proves valuable for filtering irrelevant images. Using a **confidence threshold of 0.8-0.9** to exclude logos, decorative elements, and abstract graphics reduces vision API costs by 30-50% without impacting recall. Azure Computer Vision's tagging API or a simple custom classifier trained on your specific content types works well here.

Query routing determines whether to include raw images in the generation context. A lightweight classifier or LLM prompt can categorize queries as TEXT_ONLY, IMAGE_REQUIRED, or HYBRID. Vision-only queries like "What does the settings button look like?" require the actual screenshot, while text-based questions like "How do I share a file?" typically need only the caption descriptions. This selective inclusion keeps inference costs manageable—**including a raw image adds approximately $0.05-0.15 per query** versus $0.001-0.01 for text-only context.

---

## Framework support enables rapid implementation

LangChain's MultiVectorRetriever provides the foundation for linking summaries to raw content. The pattern stores caption embeddings in the vector store while maintaining references to original images via document IDs, enabling retrieval of the caption for semantic search and the raw image for generation:

```python
retriever = MultiVectorRetriever(
    vectorstore=qdrant_vectorstore,  # Caption embeddings
    docstore=document_store,          # Raw images and full text
    id_key="doc_id"
)
```

LlamaIndex offers dedicated multi-modal capabilities through MultiModalVectorStoreIndex, which maintains separate stores for text and image embeddings. The SimpleMultiModalQueryEngine handles synthesis from mixed content automatically.

For advanced visual retrieval, ColPali and ColQwen2 represent the cutting edge. These models create multi-vector embeddings directly from document page images, bypassing OCR entirely. ColQwen2's dynamic resolution handling preserves aspect ratios better than ColPali's fixed-size approach. Qdrant's native support for multi-vector search with MaxSim scoring makes integration straightforward, though storage requirements increase substantially—expect approximately **512,000 vectors for 500 pages** versus 500 vectors with the caption approach.

---

## Practical implementation requires attention to caching and cost control

The ingestion pipeline should process images in batches of 5-10 (respecting API rate limits) with exponential backoff retry logic. Hash-based caching prevents redundant vision API calls—generate an MD5 hash of each image and store it alongside the caption with a prompt version identifier. This enables efficient re-processing when prompts change while avoiding recomputation for unchanged images.

```python
cache_key = f"caption:{image_hash}:{prompt_version}"
if cached := redis.get(cache_key):
    return json.loads(cached)
caption = vision_model.generate(image, prompt)
redis.setex(cache_key, 30*86400, json.dumps(caption))  # 30-day TTL
```

Cost monitoring should track vision API tokens separately from embedding and inference costs. For your scale, self-hosting Qwen3-embedding-8b provides **98% cost reduction** versus cloud embedding APIs. Vision API costs for initial captioning remain minimal—under $2 total for 800 images with Claude 3.5 Sonnet, under $0.35 with Gemini Flash.

Latency targets for production systems should aim for **p50 under 300ms** and **p95 under 2 seconds** end-to-end. Qdrant achieves approximately 1,238 queries per second at 3.5ms for 1M vectors with 1536 dimensions. Quantization (scalar or binary) can reduce storage by 16-32x while maintaining 96% of full-precision performance.

---

## Evaluation methodology validates system effectiveness

Testing multimodal RAG requires a balanced evaluation dataset: approximately 40% text-only questions, 40% requiring both text and images, and 20% pure visual questions. Key metrics include **source_recall@k** (percentage of queries where the correct source document appears in top-k results), **image_recall@k** (percentage where expected images are retrieved), and **cited_image_precision** (accuracy of image citations in generated responses).

LLM-as-judge evaluation works well for caption quality assessment. Present the image alongside its generated caption to a separate model and ask it to score completeness (all UI elements described), accuracy (element names and types correct), and usefulness (would this help answer UI questions) on 1-5 scales.

For A/B testing improvements, compare separate versus inline image chunks (separate typically wins), test different levels of surrounding text context inclusion, and evaluate alternative vision models for captioning quality. The Microsoft ISE team's experimentation framework provides a solid template: define metrics, run controlled experiments, measure statistical significance.

---

## Recommended implementation path for your system

Given your stack of Mistral Large via OpenRouter, Qwen3-embedding-8b, and Qdrant with hybrid search, the recommended approach minimizes disruption while maximizing capability. Start with caption-enriched text chunks using Gemini 2.5 Flash Batch for initial captioning—this can be accomplished in a single batch job costing under $1.

Structure the ingestion pipeline to extract images from documents, filter irrelevant graphics using a simple classifier, generate detailed UI-specific captions, and store them as separate chunks with metadata linking to the original image URLs. Your existing text chunking and embedding pipeline handles the captions without modification.

For inference, retrieve top-k chunks using your existing hybrid search, then check if any retrieved chunks are image captions. For queries classified as visual, fetch the corresponding raw images and include them in the Mistral Large context. The selective vision approach keeps typical query costs low while providing visual capability when needed.

Target evaluation benchmarks should be **source recall@5 above 90%**, **image recall@5 above 85%**, and **p95 latency under 2 seconds**. With 300-800 screenshots and 128 documents, single-node Qdrant easily handles the load with approximately 500MB storage for 4096-dimensional embeddings.

---

## Conclusion

The multimodal RAG landscape in 2025 favors pragmatic hybrid approaches over complex end-to-end multimodal systems. For documentation assistants with UI screenshots, **pre-captioning with vision models provides the best quality-cost-complexity tradeoff**, integrating smoothly with existing text-based RAG pipelines. The key innovations enabling this are batch processing APIs cutting costs by 50%, improved vision model understanding of UI elements, and framework support for multi-vector retrieval patterns.

Your existing Qwen3-embedding-8b and Qdrant stack requires minimal changes—the primary addition is a one-time batch captioning job and modified ingestion logic to create image chunks. The selective runtime vision pattern preserves fast response times for typical queries while enabling visual context when users specifically need it. With proper caching and cost monitoring, production systems achieve strong retrieval performance at costs measured in cents per thousand queries rather than dollars.