#!/usr/bin/env python3
"""Script to ingest documentation from data/docs/ into the system."""

import argparse
from pathlib import Path

from app.rag.chunker import chunk_text
from app.rag.retriever import QdrantRetriever


def load_documents(directory: str) -> list[dict]:
    """Load markdown documents from a directory recursively.

    Args:
        directory: Path to the directory containing .md files

    Returns:
        List of dicts with keys: title, source, product, content
    """
    documents = []
    base_path = Path(directory)

    for md_file in base_path.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        lines = text.split("\n")

        # Extract title from first line (after "# ")
        title = ""
        if lines and lines[0].startswith("# "):
            title = lines[0][2:].strip()

        # Extract source URL from second line (after "Source: ")
        source = ""
        if len(lines) > 1 and lines[2].startswith("Source: "):
            source = lines[2][8:].strip()

        # Extract product from parent folder name
        product = md_file.parent.name

        # Extract content after "---"
        content = ""
        separator_index = None
        for i, line in enumerate(lines):
            if line.strip() == "---":
                separator_index = i
                break

        if separator_index is not None:
            content = "\n".join(lines[separator_index + 1 :]).strip()
        else:
            # Fallback: use all content after title and source
            content = "\n".join(lines[4:]).strip()

        documents.append(
            {
                "title": title,
                "source": source,
                "product": product,
                "content": content,
            }
        )

    return documents


def main() -> None:
    """Main entry point for the ingest script."""
    parser = argparse.ArgumentParser(description="Ingest documentation into the system")
    parser.add_argument(
        "--source",
        type=str,
        default="data/docs",
        help="Source directory containing .md files (default: data/docs)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only load and display documents, don't ingest",
    )

    args = parser.parse_args()

    documents = load_documents(args.source)

    if args.dry_run:
        print(f"Found {len(documents)} documents\n")
        for doc in documents[:5]:  # Show first 5 for dry run
            print(f"Title: {doc['title']}")
            print(f"Source: {doc['source']}")
            print(f"Product: {doc['product']}")
            print(f"Content preview: {doc['content'][:100]}...")
            print("-" * 40)
    else:
        print(f"Loaded {len(documents)} documents")

        # Initialize retriever and create collection
        retriever = QdrantRetriever()
        retriever.create_collection()
        print(f"Collection '{retriever.collection_name}' ready")

        # Chunk all documents
        all_chunks = []
        for doc in documents:
            metadata = {
                "title": doc["title"],
                "source": doc["source"],
                "product": doc["product"],
            }
            chunks = chunk_text(doc["content"], metadata)
            all_chunks.extend(chunks)

        print(f"Created {len(all_chunks)} chunks from {len(documents)} documents")

        # Upsert chunks to Qdrant
        count = retriever.upsert(all_chunks)
        print(f"Ingested {count} chunks into Qdrant")


if __name__ == "__main__":
    main()
