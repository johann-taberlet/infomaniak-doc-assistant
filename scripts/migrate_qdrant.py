#!/usr/bin/env python3
"""Migrate Qdrant data from local instance to cloud.

Requires environment variables (from .env file):
- QDRANT_CLOUD_URL: Qdrant Cloud cluster URL
- QDRANT_CLOUD_API_KEY: Qdrant Cloud API key
- QDRANT_COLLECTION: Collection name (default: infomaniak_docs)
"""

import os
import sys

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Load environment variables from .env file
load_dotenv()

# Configuration from environment
QDRANT_CLOUD_URL = os.getenv("QDRANT_CLOUD_URL")
QDRANT_CLOUD_API_KEY = os.getenv("QDRANT_CLOUD_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "infomaniak_docs")
LOCAL_QDRANT_URL = os.getenv("QDRANT_HOST", "http://localhost:6333")


def migrate():
    """Migrate vectors from local Qdrant to Qdrant Cloud."""
    # Validate required environment variables
    if not QDRANT_CLOUD_URL:
        print("Error: QDRANT_CLOUD_URL environment variable is required")
        print("Add it to your .env file")
        sys.exit(1)

    if not QDRANT_CLOUD_API_KEY:
        print("Error: QDRANT_CLOUD_API_KEY environment variable is required")
        print("Add it to your .env file")
        sys.exit(1)

    print(f"Source: {LOCAL_QDRANT_URL}")
    print(f"Destination: {QDRANT_CLOUD_URL}")
    print(f"Collection: {COLLECTION_NAME}")
    print()

    # Source: Local Qdrant
    source = QdrantClient(url=LOCAL_QDRANT_URL)

    # Destination: Qdrant Cloud
    dest = QdrantClient(
        url=QDRANT_CLOUD_URL,
        api_key=QDRANT_CLOUD_API_KEY,
    )

    # Get collection info from source
    source_info = source.get_collection(COLLECTION_NAME)
    print(f"Source collection: {source_info.points_count} points")

    # Check if destination collection exists
    dest_collections = [c.name for c in dest.get_collections().collections]

    if COLLECTION_NAME not in dest_collections:
        # Create collection in destination with same config
        print(f"Creating collection '{COLLECTION_NAME}' in destination...")
        dest.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=source_info.config.params.vectors.size,
                distance=Distance.COSINE,
            ),
        )
        print("Collection created.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists in destination.")

    # Scroll through all points and migrate
    print("Migrating points...")
    offset = None
    total_migrated = 0
    batch_size = 100

    while True:
        points, offset = source.scroll(
            collection_name=COLLECTION_NAME,
            limit=batch_size,
            offset=offset,
            with_vectors=True,
            with_payload=True,
        )

        if not points:
            break

        # Convert Records to PointStructs and upsert to destination
        point_structs = [
            PointStruct(
                id=record.id,
                vector=record.vector,
                payload=record.payload,
            )
            for record in points
        ]
        dest.upsert(
            collection_name=COLLECTION_NAME,
            points=point_structs,
        )

        total_migrated += len(points)
        print(f"  Migrated {total_migrated} points...")

        if offset is None:
            break

    # Verify
    dest_info = dest.get_collection(COLLECTION_NAME)
    print(f"\nMigration complete!")
    print(f"  Source: {source_info.points_count} points")
    print(f"  Destination: {dest_info.points_count} points")


if __name__ == "__main__":
    migrate()
