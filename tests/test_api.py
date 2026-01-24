"""
Tests for API endpoints.

These tests verify the API contract with the frontend,
particularly the Vercel AI SDK streaming format.
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for /health endpoint."""

    def test_health_returns_ok(self, client):
        """Health endpoint should return status ok."""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestRootEndpoint:
    """Tests for / root endpoint."""

    def test_root_returns_api_info(self, client):
        """Root should return API metadata."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["docs"] == "/docs"


class TestChatEndpoint:
    """Tests for /api/chat endpoint."""

    def test_chat_requires_messages(self, client):
        """Should return 422 when messages missing."""
        response = client.post("/api/chat", json={})

        assert response.status_code == 422

    def test_chat_requires_user_message(self, client):
        """Should return 400 when no user message in history."""
        response = client.post(
            "/api/chat",
            json={"messages": [{"role": "assistant", "content": "Hello"}]},
        )

        assert response.status_code == 400
        assert "No user message" in response.json()["detail"]

    def test_chat_rejects_empty_messages(self, client):
        """Should return 400 for empty messages array."""
        response = client.post("/api/chat", json={"messages": []})

        assert response.status_code == 400


class TestCollectionsEndpoint:
    """Tests for /api/collections endpoint."""

    def test_collections_returns_list(self, client):
        """Should return collections list (may be empty if Qdrant not running)."""
        response = client.get("/api/collections")

        assert response.status_code == 200
        data = response.json()
        assert "collections" in data
        assert isinstance(data["collections"], list)
