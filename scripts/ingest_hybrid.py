#!/usr/bin/env python3
"""
Ingest documents into Qdrant with hybrid (dense + sparse) vectors.

This script creates collections with both dense embeddings and BM25 sparse vectors
for hybrid search with RRF fusion.

Usage:
    uv run python scripts/ingest_hybrid.py
    uv run python scripts/ingest_hybrid.py --strategy full_document --dataset cleaned_no_images
    uv run python scripts/ingest_hybrid.py --collection my_hybrid_experiment --recreate

Examples:
    # Default: full document strategy with no-images dataset
    uv run python scripts/ingest_hybrid.py

    # With normalization for BM25
    uv run python scripts/ingest_hybrid.py --enable-normalization

    # Custom collection name
    uv run python scripts/ingest_hybrid.py --collection infomaniak_hybrid_test --recreate
"""

import argparse
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.app.core.config import ChunkingStrategy, settings
from backend.app.rag.chunking import Chunk, Document, get_chunker
from backend.app.rag.embeddings import get_embedding_dimension
from backend.app.rag.hybrid_retriever import HybridConfig, HybridRetriever, RetrievalMode


def load_documents(dataset_path: Path) -> list[Document]:
    """
    Load all markdown documents from the dataset directory.

    Args:
        dataset_path: Path to dataset directory (e.g., data/cleaned)

    Returns:
        List of Document objects
    """
    documents = []

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    # Load from each product subdirectory
    for product_dir in sorted(dataset_path.iterdir()):
        if not product_dir.is_dir():
            continue

        for md_file in sorted(product_dir.glob("*.md")):
            content = md_file.read_text(encoding="utf-8")
            documents.append(
                Document(
                    content=content,
                    metadata={
                        "source": str(md_file.relative_to(dataset_path)),
                        "product": product_dir.name,
                    },
                )
            )

    return documents


def get_hybrid_collection_name(
    strategy: ChunkingStrategy,
    chunk_size: int,
    dataset: str,
) -> str:
    """
    Generate a hybrid collection name.

    Format: infomaniak_hybrid_{strategy}_{dataset_suffix}
    """
    dataset_suffix = "images" if dataset == "cleaned" else "no_images"

    if strategy == ChunkingStrategy.FULL_DOCUMENT:
        return f"infomaniak_hybrid_full_doc_{dataset_suffix}"

    if strategy == ChunkingStrategy.SEMANTIC:
        return f"infomaniak_hybrid_semantic_{dataset_suffix}"

    return f"infomaniak_hybrid_{strategy.value}_{chunk_size}_{dataset_suffix}"


def main():
    parser = argparse.ArgumentParser(
        description="Ingest documents with hybrid (dense + sparse) vectors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default=settings.dataset_path,
        choices=["cleaned", "cleaned_no_images"],
        help="Dataset to ingest (default: %(default)s)",
    )
    parser.add_argument(
        "--strategy",
        type=str,
        default="full_document",
        choices=[s.value for s in ChunkingStrategy],
        help="Chunking strategy (default: %(default)s)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=settings.chunk_size,
        help="Chunk size in characters (default: %(default)s)",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=settings.chunk_overlap,
        help="Chunk overlap in characters (default: %(default)s)",
    )
    parser.add_argument(
        "--window-size",
        type=int,
        default=settings.sentence_window_size,
        help="Sentence window size for sentence_window strategy (default: %(default)s)",
    )
    parser.add_argument(
        "--collection",
        type=str,
        default=None,
        help="Collection name (auto-generated if not specified)",
    )
    parser.add_argument(
        "--enable-normalization",
        action="store_true",
        help="Enable BM25 vocabulary normalization during indexing",
    )
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Recreate collection if it exists",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually ingesting",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Batch size for embedding generation (default: %(default)s)",
    )

    args = parser.parse_args()

    # Determine collection name
    strategy = ChunkingStrategy(args.strategy)
    collection_name = args.collection or get_hybrid_collection_name(
        strategy=strategy,
        chunk_size=args.chunk_size,
        dataset=args.dataset,
    )

    print("=" * 60)
    print("Hybrid Document Ingestion")
    print("=" * 60)
    print(f"Dataset:           {args.dataset}")
    print(f"Strategy:          {args.strategy}")
    print(f"Chunk size:        {args.chunk_size}")
    print(f"Chunk overlap:     {args.chunk_overlap}")
    print(f"Collection:        {collection_name}")
    print(f"Normalization:     {args.enable_normalization}")
    print(f"Recreate:          {args.recreate}")
    print(f"Dry run:           {args.dry_run}")
    print()

    # Load documents
    dataset_path = Path("data") / args.dataset
    print(f"Loading documents from {dataset_path}...")
    documents = load_documents(dataset_path)
    print(f"  Loaded {len(documents)} documents")

    # Get chunker
    chunker = get_chunker(
        strategy=args.strategy,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        window_size=args.window_size,
    )
    print(f"  Using chunker: {type(chunker).__name__}")

    # Chunk documents
    print("Chunking documents...")
    chunks: list[Chunk] = chunker.chunk(documents)
    print(f"  Created {len(chunks)} chunks")

    # Calculate stats
    chunk_lengths = [len(c.content) for c in chunks]
    avg_length = sum(chunk_lengths) / len(chunk_lengths) if chunk_lengths else 0
    min_length = min(chunk_lengths) if chunk_lengths else 0
    max_length = max(chunk_lengths) if chunk_lengths else 0

    print(f"  Avg chunk length: {avg_length:.0f} chars")
    print(f"  Min chunk length: {min_length} chars")
    print(f"  Max chunk length: {max_length} chars")

    if args.dry_run:
        print("\n[DRY RUN] Would ingest chunks to Qdrant")
        print(f"[DRY RUN] Collection: {collection_name}")
        print(f"[DRY RUN] Dense vector dimension: {get_embedding_dimension()}")
        print(f"[DRY RUN] Sparse vectors: BM25 ({settings.bm25_model})")

        # Show sample chunks
        print("\nSample chunks:")
        for i, chunk in enumerate(chunks[:3]):
            print(f"\n--- Chunk {i + 1} ---")
            print(f"Metadata: {chunk.metadata}")
            print(f"Content preview: {chunk.content[:200]}...")

        return

    # Initialize hybrid retriever
    print(f"\nInitializing hybrid collection: {collection_name}")

    config = HybridConfig(
        mode=RetrievalMode.HYBRID,
        enable_normalization=args.enable_normalization,
    )
    retriever = HybridRetriever(collection_name=collection_name, config=config)

    vector_size = get_embedding_dimension()
    print(f"  Dense vector dimension: {vector_size}")
    print(f"  Sparse vectors: BM25 ({settings.bm25_model})")

    retriever.create_collection(
        dense_vector_size=vector_size,
        recreate=args.recreate,
    )

    # Check if collection already has data
    info = retriever.get_collection_info()
    if info.get("points_count", 0) > 0 and not args.recreate:
        print(f"  Collection already has {info['points_count']} points")
        print("  Use --recreate to replace existing data")
        return

    # Add chunks to collection
    print("\nEmbedding and storing chunks (dense + sparse)...")
    num_added = retriever.add_chunks(
        chunks,
        batch_size=args.batch_size,
        show_progress=True,
    )

    print(f"\nIngestion complete!")
    print(f"  Documents: {len(documents)}")
    print(f"  Chunks: {num_added}")
    print(f"  Collection: {collection_name}")

    # Verify
    info = retriever.get_collection_info()
    print(f"  Verified points in collection: {info.get('points_count', 'unknown')}")

    # Test search
    print("\nTesting hybrid search...")
    test_query = "Comment synchroniser kDrive ?"
    results = retriever.search(test_query, top_k=3)
    print(f"  Query: {test_query}")
    print(f"  Results: {len(results)}")
    for i, r in enumerate(results):
        print(f"    {i + 1}. Score: {r.score:.4f} - {r.content[:60]}...")


if __name__ == "__main__":
    main()
