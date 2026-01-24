"""Tests for the fake database."""

import pytest

from backend.app.agents.fakedb import (
    CHANNELS,
    CONTACTS,
    FILES,
    FOLDERS,
    MEETINGS,
    get_fakedb,
    reset_fakedb,
)


class TestFakeDBSeedData:
    """Tests for seed data presence and structure."""

    def test_contacts_count(self):
        """Test that we have at least 5 contacts."""
        assert len(CONTACTS) >= 5

    def test_contacts_have_required_fields(self):
        """Test that contacts have required fields."""
        for contact in CONTACTS:
            assert "id" in contact
            assert "name" in contact
            assert "email" in contact

    def test_files_count(self):
        """Test that we have at least 5 files."""
        assert len(FILES) >= 5

    def test_files_have_required_fields(self):
        """Test that files have required fields."""
        for file in FILES:
            assert "id" in file
            assert "name" in file
            assert "type" in file

    def test_folders_count(self):
        """Test that we have at least 3 folders."""
        assert len(FOLDERS) >= 3

    def test_channels_count(self):
        """Test that we have at least 4 channels."""
        assert len(CHANNELS) >= 4

    def test_channel_types(self):
        """Test that channels have different types."""
        types = {channel["type"] for channel in CHANNELS}
        assert "public" in types
        assert "direct" in types

    def test_meetings_count(self):
        """Test that we have sample meetings."""
        assert len(MEETINGS) >= 1


class TestFakeDBQueries:
    """Tests for FakeDB query functionality."""

    @pytest.fixture
    def db(self):
        """Get a fresh FakeDB instance."""
        return reset_fakedb()

    def test_query_all_contacts(self, db):
        """Test querying all contacts without filter."""
        results = db.query("contacts")
        assert len(results) == len(CONTACTS)

    def test_query_exact_match(self, db):
        """Test exact match filter."""
        results = db.query("contacts", {"name": "John Smith"})
        assert len(results) == 1
        assert results[0]["name"] == "John Smith"

    def test_query_contains_case_insensitive(self, db):
        """Test contains filter is case-insensitive."""
        # "john" matches both "John Smith" and "Sarah Johnson"
        results = db.query("contacts", {"name_contains": "john"})
        assert len(results) == 2
        names = {r["name"] for r in results}
        assert "John Smith" in names
        assert "Sarah Johnson" in names

        # Also works with uppercase
        results = db.query("contacts", {"name_contains": "SMITH"})
        assert len(results) == 1
        assert results[0]["name"] == "John Smith"

    def test_query_contains_partial_match(self, db):
        """Test contains filter matches substring."""
        results = db.query("contacts", {"email_contains": "@example.com"})
        assert len(results) == len(CONTACTS)  # All have this domain

    def test_query_multiple_filters_and(self, db):
        """Test multiple filters are combined with AND."""
        results = db.query("files", {"type": "document", "folder_id": "folder_1"})
        # Only report.pdf matches both conditions
        assert len(results) == 1
        assert results[0]["name"] == "report.pdf"

    def test_query_no_match(self, db):
        """Test query with no matching results."""
        results = db.query("contacts", {"name": "Nonexistent Person"})
        assert len(results) == 0

    def test_query_unknown_collection_raises(self, db):
        """Test that querying unknown collection raises ValueError."""
        with pytest.raises(ValueError, match="Unknown collection"):
            db.query("unknown_collection")

    def test_query_files_by_type(self, db):
        """Test querying files by type."""
        results = db.query("files", {"type": "document"})
        assert len(results) == 2  # report.pdf and meeting-notes.docx

    def test_query_channels_by_type(self, db):
        """Test querying channels by type."""
        results = db.query("channels", {"type": "direct"})
        assert len(results) == 2  # dm_david and dm_sarah

    def test_query_meetings_by_host(self, db):
        """Test querying meetings by host."""
        results = db.query("meetings", {"host_id": "contact_1"})
        assert len(results) == 1
        assert results[0]["title"] == "Weekly Standup"


class TestFakeDBHelpers:
    """Tests for FakeDB helper methods."""

    @pytest.fixture
    def db(self):
        """Get a fresh FakeDB instance."""
        return reset_fakedb()

    def test_list_collections(self, db):
        """Test listing all collections."""
        collections = db.list_collections()
        assert "contacts" in collections
        assert "files" in collections
        assert "folders" in collections
        assert "channels" in collections
        assert "messages" in collections
        assert "meetings" in collections

    def test_get_collection(self, db):
        """Test getting a collection by name."""
        contacts = db.get_collection("contacts")
        assert contacts is not None
        assert len(contacts) == len(CONTACTS)

    def test_get_nonexistent_collection(self, db):
        """Test getting a nonexistent collection."""
        result = db.get_collection("nonexistent")
        assert result is None


class TestFakeDBSingleton:
    """Tests for FakeDB singleton behavior."""

    def test_get_fakedb_returns_same_instance(self):
        """Test that get_fakedb returns the same instance."""
        reset_fakedb()  # Reset first to ensure clean state
        db1 = get_fakedb()
        db2 = get_fakedb()
        assert db1 is db2

    def test_reset_fakedb_creates_new_instance(self):
        """Test that reset_fakedb creates a new instance."""
        db1 = get_fakedb()
        db2 = reset_fakedb()
        db3 = get_fakedb()

        assert db1 is not db2
        assert db2 is db3
