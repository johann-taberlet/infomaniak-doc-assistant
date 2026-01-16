"""Tests for FastAPI endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_200():
    """Test that health endpoint returns 200 with status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_rejects_empty_message():
    """Test that chat endpoint rejects empty message with 400."""
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 400
