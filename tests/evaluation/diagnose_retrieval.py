"""Diagnose retrieval failures by testing each RAG step."""

import sys
sys.path.insert(0, ".")

from app.rag.retriever import QdrantRetriever
from app.rag.embeddings import embed_text
from app.rag.query_expansion import expand_query
from app.config import settings

# Failing queries to diagnose (source is URL pattern to match)
FAILING_QUERIES = [
    {
        "id": "Q5",
        "question": "How do I sign a PDF document in kDrive?",
        "expected_source": "1463/sign-a-pdf",
        "type": "retrieval_failure",
    },
    {
        "id": "Q13",
        "question": "How do I restore my entire kDrive to a previous state (rewind)?",
        "expected_source": "1838/restore-kdrive-to-a-previous-state",
        "type": "retrieval_failure",
    },
    {
        "id": "Q15",
        "question": "How do I set a reminder for a kChat message?",
        "expected_source": "1664/create-a-kchat-message-reminder",
        "type": "wrong_topic",
    },
    {
        "id": "Q7",
        "question": "How can I search for files within kDrive?",
        "expected_source": "2320/search-for-data-on-kdrive",
        "type": "partial",
    },
    {
        "id": "Q12",
        "question": "How do I manage deleted files and the trash in kDrive?",
        "expected_source": "2383/manage-kdrive-file-deletion",
        "type": "partial",
    },
]


def check_document_in_collection(retriever: QdrantRetriever, source_file: str) -> dict:
    """Check if a document exists in the Qdrant collection."""
    # Search for documents with matching source
    result = retriever.client.scroll(
        collection_name=retriever.collection_name,
        scroll_filter={
            "must": [
                {"key": "source", "match": {"text": source_file}}
            ]
        },
        limit=100,
        with_payload=True,
        with_vectors=False,
    )

    points, _ = result
    return {
        "exists": len(points) > 0,
        "chunk_count": len(points),
        "chunks": [
            {
                "id": str(p.id),
                "title": p.payload.get("title", ""),
                "content_preview": p.payload.get("content", "")[:200] + "..."
            }
            for p in points
        ]
    }


def diagnose_query(retriever: QdrantRetriever, query_info: dict) -> dict:
    """Run full diagnosis on a query."""
    query = query_info["question"]
    expected_source = query_info["expected_source"]

    print(f"\n{'='*80}")
    print(f"DIAGNOSING: {query_info['id']} - {query_info['type'].upper()}")
    print(f"Query: {query}")
    print(f"Expected source: {expected_source}")
    print(f"{'='*80}")

    results = {"query": query, "expected_source": expected_source}

    # Step 1: Check if document exists in collection
    print("\n[STEP 1] Checking if expected document exists in collection...")
    doc_check = check_document_in_collection(retriever, expected_source)
    results["document_in_collection"] = doc_check
    if doc_check["exists"]:
        print(f"  ✓ Document EXISTS with {doc_check['chunk_count']} chunk(s)")
        for i, chunk in enumerate(doc_check["chunks"][:2]):
            print(f"    Chunk {i+1}: {chunk['content_preview'][:100]}...")
    else:
        print(f"  ✗ Document NOT FOUND in collection!")
        return results

    # Step 2: Query expansion
    print("\n[STEP 2] Query expansion...")
    expanded_query = expand_query(query)
    results["expanded_query"] = expanded_query
    print(f"  Original: {query}")
    print(f"  Expanded: {expanded_query}")

    # Step 3: Vector search results
    print("\n[STEP 3] Vector search (top 15)...")
    vector_results = retriever._search_vector(query, 15)
    results["vector_results"] = []
    expected_found_vector = False
    expected_rank_vector = None

    for rank, (doc_id, score, payload) in enumerate(vector_results):
        source = payload.get("source", "")
        title = payload.get("title", "")
        is_expected = expected_source in source
        if is_expected:
            expected_found_vector = True
            expected_rank_vector = rank + 1
        marker = ">>> " if is_expected else "    "
        print(f"  {marker}{rank+1}. [{score:.4f}] {source[:50]}")
        results["vector_results"].append({
            "rank": rank + 1,
            "score": score,
            "source": source,
            "title": title,
            "is_expected": is_expected,
        })

    if expected_found_vector:
        print(f"  ✓ Expected doc found at rank {expected_rank_vector}")
    else:
        print(f"  ✗ Expected doc NOT in top 15 vector results")

    # Step 4: BM25 search results
    print("\n[STEP 4] BM25 search (top 15)...")
    bm25_results = retriever._search_bm25(expanded_query, 15)
    results["bm25_results"] = []
    expected_found_bm25 = False
    expected_rank_bm25 = None

    # Need to fetch payloads for BM25 results
    for rank, (doc_id, score) in enumerate(bm25_results):
        points = retriever.client.retrieve(
            collection_name=retriever.collection_name,
            ids=[doc_id],
            with_payload=True,
        )
        payload = points[0].payload if points else {}
        source = payload.get("source", "")
        title = payload.get("title", "")
        is_expected = expected_source in source
        if is_expected:
            expected_found_bm25 = True
            expected_rank_bm25 = rank + 1
        marker = ">>> " if is_expected else "    "
        print(f"  {marker}{rank+1}. [{score:.4f}] {source[:50]}")
        results["bm25_results"].append({
            "rank": rank + 1,
            "score": score,
            "source": source,
            "title": title,
            "is_expected": is_expected,
        })

    if expected_found_bm25:
        print(f"  ✓ Expected doc found at rank {expected_rank_bm25}")
    else:
        print(f"  ✗ Expected doc NOT in top 15 BM25 results")

    # Step 5: Final hybrid search results
    print("\n[STEP 5] Final hybrid search (top 15)...")
    final_docs = retriever.search(query, top_k=15)
    results["final_results"] = []
    expected_found_final = False
    expected_rank_final = None

    for rank, doc in enumerate(final_docs):
        source = doc.metadata.get("source", "")
        score = doc.metadata.get("score", 0)
        is_expected = expected_source in source
        if is_expected:
            expected_found_final = True
            expected_rank_final = rank + 1
        marker = ">>> " if is_expected else "    "
        print(f"  {marker}{rank+1}. [{score:.4f}] {source[:50]}")
        results["final_results"].append({
            "rank": rank + 1,
            "score": score,
            "source": source,
            "is_expected": is_expected,
        })

    if expected_found_final:
        print(f"  ✓ Expected doc found at rank {expected_rank_final}")
    else:
        print(f"  ✗ Expected doc NOT in top 15 final results")

    # Summary
    print("\n[SUMMARY]")
    results["summary"] = {
        "in_collection": doc_check["exists"],
        "vector_rank": expected_rank_vector,
        "bm25_rank": expected_rank_bm25,
        "final_rank": expected_rank_final,
    }
    print(f"  In collection: {doc_check['exists']}")
    print(f"  Vector rank: {expected_rank_vector or 'NOT FOUND'}")
    print(f"  BM25 rank: {expected_rank_bm25 or 'NOT FOUND'}")
    print(f"  Final rank: {expected_rank_final or 'NOT FOUND'}")

    return results


def main():
    print("RAG Retrieval Diagnostics")
    print(f"Collection: {settings.QDRANT_COLLECTION}")
    print(f"Hybrid enabled: {settings.RAG_HYBRID_ENABLED}")
    print(f"Top K: {settings.RAG_TOP_K}")

    retriever = QdrantRetriever()

    all_results = {}
    for query_info in FAILING_QUERIES:
        results = diagnose_query(retriever, query_info)
        all_results[query_info["id"]] = results

    # Final summary table
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"{'ID':<5} {'Type':<18} {'In DB':<6} {'Vector':<8} {'BM25':<8} {'Final':<8}")
    print("-"*60)
    for query_info in FAILING_QUERIES:
        qid = query_info["id"]
        qtype = query_info["type"]
        s = all_results[qid]["summary"]
        in_db = "✓" if s["in_collection"] else "✗"
        vec = str(s["vector_rank"]) if s["vector_rank"] else "✗"
        bm25 = str(s["bm25_rank"]) if s["bm25_rank"] else "✗"
        final = str(s["final_rank"]) if s["final_rank"] else "✗"
        print(f"{qid:<5} {qtype:<18} {in_db:<6} {vec:<8} {bm25:<8} {final:<8}")


if __name__ == "__main__":
    main()
