"""Fake database with seed data for agent interactions.

This module provides a simulated database that the agent can query.
The backend maintains a copy so the agent can make decisions based on query results.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any

# Seed data matching PRD Section 4.4


CONTACTS = [
    {
        "id": "contact_1",
        "name": "John Smith",
        "email": "john.smith@example.com",
        "avatar": "/avatars/john.png",
        "status": "online",
    },
    {
        "id": "contact_2",
        "name": "Sarah Johnson",
        "email": "sarah.johnson@example.com",
        "avatar": "/avatars/sarah.png",
        "status": "away",
    },
    {
        "id": "contact_3",
        "name": "David Chen",
        "email": "david.chen@example.com",
        "avatar": "/avatars/david.png",
        "status": "offline",
    },
    {
        "id": "contact_4",
        "name": "Marie Dubois",
        "email": "marie.dubois@example.com",
        "avatar": "/avatars/marie.png",
        "status": "online",
    },
    {
        "id": "contact_5",
        "name": "Marketing Team",
        "email": "marketing@example.com",
        "avatar": "/avatars/team.png",
        "status": "online",
        "is_group": True,
    },
]

FILES = [
    {
        "id": "file_1",
        "name": "budget.xlsx",
        "type": "spreadsheet",
        "size": 245760,
        "folder_id": "folder_1",
        "created_at": "2024-01-15T10:30:00Z",
        "modified_at": "2024-01-20T14:22:00Z",
        "owner_id": "contact_1",
    },
    {
        "id": "file_2",
        "name": "presentation.pptx",
        "type": "presentation",
        "size": 5242880,
        "folder_id": "folder_2",
        "created_at": "2024-01-10T09:00:00Z",
        "modified_at": "2024-01-18T16:45:00Z",
        "owner_id": "contact_2",
    },
    {
        "id": "file_3",
        "name": "report.pdf",
        "type": "document",
        "size": 1048576,
        "folder_id": "folder_1",
        "created_at": "2024-01-05T11:15:00Z",
        "modified_at": "2024-01-05T11:15:00Z",
        "owner_id": "contact_3",
    },
    {
        "id": "file_4",
        "name": "meeting-notes.docx",
        "type": "document",
        "size": 32768,
        "folder_id": "folder_2",
        "created_at": "2024-01-22T09:30:00Z",
        "modified_at": "2024-01-22T10:00:00Z",
        "owner_id": "contact_1",
    },
    {
        "id": "file_5",
        "name": "logo.png",
        "type": "image",
        "size": 153600,
        "folder_id": "folder_3",
        "created_at": "2023-12-01T08:00:00Z",
        "modified_at": "2023-12-01T08:00:00Z",
        "owner_id": "contact_5",
    },
]

FOLDERS = [
    {
        "id": "folder_1",
        "name": "My Files",
        "parent_id": None,
        "owner_id": "contact_1",
    },
    {
        "id": "folder_2",
        "name": "Projects",
        "parent_id": "folder_1",
        "owner_id": "contact_1",
    },
    {
        "id": "folder_3",
        "name": "Shared",
        "parent_id": None,
        "owner_id": "contact_5",
        "shared_with": ["contact_1", "contact_2", "contact_3", "contact_4"],
    },
]

CHANNELS = [
    {
        "id": "channel_1",
        "name": "general",
        "type": "public",
        "members": ["contact_1", "contact_2", "contact_3", "contact_4", "contact_5"],
        "unread_count": 3,
    },
    {
        "id": "channel_2",
        "name": "random",
        "type": "public",
        "members": ["contact_1", "contact_2", "contact_4"],
        "unread_count": 0,
    },
    {
        "id": "channel_3",
        "name": "dm_david",
        "type": "direct",
        "members": ["contact_1", "contact_3"],
        "unread_count": 1,
        "display_name": "David Chen",
    },
    {
        "id": "channel_4",
        "name": "dm_sarah",
        "type": "direct",
        "members": ["contact_1", "contact_2"],
        "unread_count": 0,
        "display_name": "Sarah Johnson",
    },
]

MESSAGES = [
    {
        "id": "msg_1",
        "channel_id": "channel_1",
        "sender_id": "contact_2",
        "content": "Hey everyone! Meeting at 3pm today.",
        "timestamp": "2024-01-22T09:00:00Z",
    },
    {
        "id": "msg_2",
        "channel_id": "channel_1",
        "sender_id": "contact_3",
        "content": "Sounds good, I'll be there!",
        "timestamp": "2024-01-22T09:05:00Z",
    },
    {
        "id": "msg_3",
        "channel_id": "channel_3",
        "sender_id": "contact_3",
        "content": "Can you review my PR when you get a chance?",
        "timestamp": "2024-01-22T10:30:00Z",
    },
    {
        "id": "msg_4",
        "channel_id": "channel_1",
        "sender_id": "contact_4",
        "content": "I've uploaded the new designs to the shared folder.",
        "timestamp": "2024-01-22T11:00:00Z",
    },
]

MEETINGS = [
    {
        "id": "meeting_1",
        "title": "Weekly Standup",
        "host_id": "contact_1",
        "participants": ["contact_1", "contact_2", "contact_3"],
        "scheduled_at": "2024-01-23T10:00:00Z",
        "duration_minutes": 30,
        "status": "scheduled",
    },
    {
        "id": "meeting_2",
        "title": "Project Review",
        "host_id": "contact_2",
        "participants": ["contact_1", "contact_2", "contact_4", "contact_5"],
        "scheduled_at": "2024-01-24T14:00:00Z",
        "duration_minutes": 60,
        "status": "scheduled",
    },
]


@dataclass
class FakeDB:
    """In-memory fake database for agent queries.

    Supports exact match and contains filters.
    Multiple filters are combined with AND logic.
    """

    contacts: list[dict[str, Any]] = field(default_factory=lambda: copy.deepcopy(CONTACTS))
    files: list[dict[str, Any]] = field(default_factory=lambda: copy.deepcopy(FILES))
    folders: list[dict[str, Any]] = field(default_factory=lambda: copy.deepcopy(FOLDERS))
    channels: list[dict[str, Any]] = field(default_factory=lambda: copy.deepcopy(CHANNELS))
    messages: list[dict[str, Any]] = field(default_factory=lambda: copy.deepcopy(MESSAGES))
    meetings: list[dict[str, Any]] = field(default_factory=lambda: copy.deepcopy(MEETINGS))

    def get_collection(self, name: str) -> list[dict[str, Any]] | None:
        """Get a collection by name.

        Args:
            name: Collection name (contacts, files, folders, channels, messages, meetings)

        Returns:
            List of items in the collection, or None if not found
        """
        return getattr(self, name, None)

    def query(
        self, collection: str, filters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Query a collection with optional filters.

        Supports:
        - Exact match: {"name": "John Smith"}
        - Contains (case-insensitive): {"name_contains": "john"}
        - Multiple filters combined with AND

        Args:
            collection: Name of the collection to query
            filters: Optional dict of filters to apply

        Returns:
            List of matching items

        Raises:
            ValueError: If collection doesn't exist
        """
        data = self.get_collection(collection)
        if data is None:
            raise ValueError(f"Unknown collection: {collection}")

        if not filters:
            return list(data)

        results = []
        for item in data:
            if self._matches(item, filters):
                results.append(item)
        return results

    def _matches(self, item: dict[str, Any], filters: dict[str, Any]) -> bool:
        """Check if an item matches all filters.

        Args:
            item: The item to check
            filters: Dict of filters to apply

        Returns:
            True if all filters match
        """
        for key, value in filters.items():
            if key.endswith("_contains"):
                # Contains filter (case-insensitive)
                field_name = key[:-9]  # Remove "_contains" suffix
                if field_name not in item:
                    return False
                item_value = item[field_name]
                if not isinstance(item_value, str):
                    return False
                if not isinstance(value, str):
                    return False
                if value.lower() not in item_value.lower():
                    return False
            else:
                # Exact match
                if key not in item:
                    return False
                if item[key] != value:
                    return False
        return True

    def list_collections(self) -> list[str]:
        """List all available collections.

        Returns:
            List of collection names
        """
        return ["contacts", "files", "folders", "channels", "messages", "meetings"]


# Singleton instance
_db_instance: FakeDB | None = None


def get_fakedb() -> FakeDB:
    """Get the singleton FakeDB instance.

    Returns:
        The shared FakeDB instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = FakeDB()
    return _db_instance


def reset_fakedb() -> FakeDB:
    """Reset the FakeDB to initial state (useful for testing).

    Returns:
        A fresh FakeDB instance
    """
    global _db_instance
    _db_instance = FakeDB()
    return _db_instance
