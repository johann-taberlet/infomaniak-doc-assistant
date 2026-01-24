#!/usr/bin/env python3
"""
Ingest documents into Qdrant with configurable chunking strategy.

This script loads documents from the cleaned dataset, applies a chunking
strategy, generates embeddings, and stores everything in Qdrant.

Usage:
    uv run python scripts/ingest.py
    uv run python scripts/ingest.py --strategy recursive --chunk-size 1500
    uv run python scripts/ingest.py --dataset cleaned_no_images --strategy semantic
    uv run python scripts/ingest.py --collection my_experiment --recreate

Examples:
    # Baseline experiment
    uv run python scripts/ingest.py --dataset cleaned --strategy recursive --chunk-size 1500

    # No-images experiment
    uv run python scripts/ingest.py --dataset cleaned_no_images --strategy recursive --chunk-size 1500

    # Semantic chunking experiment
    uv run python scripts/ingest.py --dataset cleaned_no_images --strategy semantic

    # Full document (no chunking) baseline
    uv run python scripts/ingest.py --dataset cleaned_no_images --strategy full_document
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
from backend.app.rag.retriever import QdrantRetriever


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


def main():
    parser = argparse.ArgumentParser(
        description="Ingest documents into Qdrant with configurable chunking",
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
        default=settings.chunking_strategy.value,
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
        "--recreate",
        action="store_true",
        help="Recreate collection if it exists",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually ingesting",
    )

    args = parser.parse_args()

    # Determine collection name
    strategy = ChunkingStrategy(args.strategy)
    collection_name = args.collection or settings.get_collection_name(
        strategy=strategy,
        chunk_size=args.chunk_size,
        dataset=args.dataset,
    )

    print("=" * 60)
    print("Document Ingestion")
    print("=" * 60)
    print(f"Dataset:        {args.dataset}")
    print(f"Strategy:       {args.strategy}")
    print(f"Chunk size:     {args.chunk_size}")
    print(f"Chunk overlap:  {args.chunk_overlap}")
    print(f"Collection:     {collection_name}")
    print(f"Recreate:       {args.recreate}")
    print(f"Dry run:        {args.dry_run}")
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
        print(f"[DRY RUN] Vector dimension: {get_embedding_dimension()}")

        # Show sample chunks
        print("\nSample chunks:")
        for i, chunk in enumerate(chunks[:3]):
            print(f"\n--- Chunk {i + 1} ---")
            print(f"Metadata: {chunk.metadata}")
            print(f"Content preview: {chunk.content[:200]}...")
            if chunk.context_window:
                print(f"Context window preview: {chunk.context_window[:200]}...")

        return

    # Initialize retriever and create collection
    print(f"\nInitializing Qdrant collection: {collection_name}")
    retriever = QdrantRetriever(collection_name=collection_name)

    vector_size = get_embedding_dimension()
    print(f"  Vector dimension: {vector_size}")

    retriever.create_collection(
        vector_size=vector_size,
        recreate=args.recreate,
    )

    # Check if collection already has data
    info = retriever.get_collection_info()
    if info.get("points_count", 0) > 0 and not args.recreate:
        print(f"  Collection already has {info['points_count']} points")
        print("  Use --recreate to replace existing data")
        return

    # Add chunks to collection
    print("\nEmbedding and storing chunks...")
    num_added = retriever.add_chunks(chunks, show_progress=True)

    print(f"\nIngestion complete!")
    print(f"  Documents: {len(documents)}")
    print(f"  Chunks: {num_added}")
    print(f"  Collection: {collection_name}")

    # Verify
    info = retriever.get_collection_info()
    print(f"  Verified points in collection: {info.get('points_count', 'unknown')}")


if __name__ == "__main__":
    main()
